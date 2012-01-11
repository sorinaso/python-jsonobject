from json import loads
from attributes import *
from utils import JSONObjectError

class JSONObjectDecoder(object):
    def __set_attr(self, attr_name, value):
        '''Setea un atributo json en el objeto'''
        try:
            setattr(self,attr_name, value)
        except AttributeError:
            raise JSONObjectError(
                'El atributo %s no existe en el objeto %s ' % (attr_name, self))

    def __get_attr(self, attr_name):
        '''Obtiene un atributo json del objeto'''
        self._json_attrs.assert_exists(attr_name)
        return getattr(self, attr_name)

    def __get_attr_of_class(self, attr_name, class_name):
        self._json_attrs.assert_class(attr_name, class_name)
        return self.__get_attr(attr_name)

    def __set_string(self, attr_name, str_value):
        '''Setea un atributo del tipo string.'''
        self._json_attrs.assert_class(attr_name, JSONStringAttribute)
        self.__set_attr(attr_name, str_value)

    def __set_list(self, attr_name, list_value):
        '''Arma una lista de atributos json esta lista si o si debe del
        tipo atributo de lista json.'''
        self._json_attrs.assert_class(attr_name, JSONListAttribute)

        new_list = []

        for e in list_value:
            if not isinstance(e, dict):
                raise JSONObjectError('Solo se soportan diccionarios '
                                'como elementos de listas' % list_value)
            else:
                o = self._json_attrs[attr_name].list_class()
                o.decode_dict(e)
                new_list.append(o)

        self.__set_attr(attr_name, new_list)

    def __set_object(self, attr_name, value):
        '''Setea un atributo del tipo objeto json, recursivamente
        lo llama para que a su vez se decodifique el mismo.'''
        o = self._json_attrs[attr_name].obj_class()
        o.decode_dict(value)
        setattr(self, attr_name, o)

    def decode_dict(self, a_dict):
        '''Decodifica el diccionario sacado a partir de json
        al objeto.'''
        for k,v in a_dict.items():
            if isinstance(v, basestring):
                self.__set_string(k, v)
            elif isinstance(v, list):
                self.__set_list(k, v)
            elif type(v) is dict:
                self.__set_object(k, v)
            else:
                raise JSONObjectError('El elemento %s tiene un tipo(%s) '
                                'que no se puede manejar' % (v.__class__,v))

    def decode(self, json):
        '''Decodifica un json al objeto.'''
        self.decode_dict(loads(json))