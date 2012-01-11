from json import loads, dumps
from attributes import *

class JSONObjectBuilder(type):
    """
    A metaclass to normalize arguments give to the get_db_prep_* and db_type
    methods on fields.
    """
    def __new__(cls, name, bases, attrs):
        new_cls = super(JSONObjectBuilder, cls).__new__(cls, name, bases, attrs)
        json_fields = {}
        
        for k,v in attrs.items():
            if isinstance(v, JSONAttribute):
                json_fields[k] = v
                v.set_name(k)
                setattr(new_cls, k, v.default_value())

        setattr(new_cls, '_json_attrs', json_fields)

        return new_cls


class JSONObject():
    __metaclass__ = JSONObjectBuilder

    def decode_dict(self, a_dict):
        '''Decodifica el diccionario sacado a partir de json
        al objeto.'''
        for k,v in self._json_attrs.items():
            try:
                setattr(self, k , v.to_python(a_dict[k]))
            except AttributeError:
                raise JSONObjectError('El atributo json(%s) no existe '
                                      'en el objeto %s', (k, self.__dict__))

    def decode(self, json):
        '''Decodifica un json al objeto.'''
        self.decode_dict(loads(json))

    def build_dict(self):
        enc_dict = {}

        for k, v in self._json_attrs.items():
            a = getattr(self, k)
            enc_dict[k] = v.to_dict_value(a)
            
        return enc_dict

    def encode(self):
        return dumps(self.build_dict())
