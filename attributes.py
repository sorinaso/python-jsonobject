from UserDict import UserDict
from utils import JSONObjectError
class JSONAttributeError(Exception):
    pass

class JSONAttribute(object):
        def assert_type(self, var):
            if not isinstance(var, self.internal_type()):
                raise JSONAttributeError(
                    'El atributo %s(%s) no es del tipo %s'
                    % (self.name, str(var),str(self.internal_type())))

        def set_name(self, name):
            self.name = name

        def internal_type(self):
            '''Tipo interno del atributo.'''
            raise NotImplemented

        def default_value(self):
            '''Valor default con el que se inicializan
            los atributos del objeto de cada tipo.'''
            raise NotImplemented

        def to_object_attribute(self, value):
            '''Convierte el valor pasado al valor que deberia
            utilizarse en el atributo cuando se decodifica el
            diccionario.'''
            raise NotImplemented

        def to_dict_value(self, value):
            '''Convierte el valor pasado al valor que deberia
            tenes en un diccionario para luego serializar a json.'''
            raise NotImplemented

class JSONStringAttribute(JSONAttribute):
    def internal_type(self):
        return basestring
    
    def default_value(self):
        return ''

    def to_object_attribute(self, value):
        self.assert_type(value)
        return unicode(value)

    def to_dict_value(self, value):
        self.assert_type(value)
        return unicode(value)
    
class JSONIntegerAttribute(JSONAttribute):
    def default_value(self):
        return None

    def internal_type(self):
        return int

    def to_object_attribute(self, value):
        self.assert_type(value)
        return value

    def to_dict_value(self, value):
        self.assert_type(value)
        return value

class JSONObjectAttribute(JSONAttribute):
    def __init__(self, obj_class):
        self.obj_class = obj_class

    def default_value(self):
        return None

    def internal_type(self):
        return self.obj_class

    def to_object_attribute(self, value):
        o = self.obj_class()
        o.decode_dict(value)
        return o
    
    def to_dict_value(self, value):
        self.assert_type(value)
        return value.build_dict()

class JSONListAttribute(JSONAttribute):
    def __init__(self, list_class):
        self.list_class = list_class

    def default_value(self):
        return None

    def internal_type(self):
        return list

    def to_object_attribute(self, value):
        new_list = []

        for e in value:
            if not isinstance(e, dict):
                raise JSONObjectError('Solo se soportan diccionarios '
                                'como elementos de listas' % list_value)
            else:
                o = self.list_class()
                o.decode_dict(e)
                new_list.append(o)

        return new_list

    def to_dict_value(self, value):
        ret = []
        
        for e in value:
            ret.append(e.build_dict())

        return ret
