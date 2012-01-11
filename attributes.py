from UserDict import UserDict
from utils import JSONObjectError
class JSONAttributeError(Exception):
    pass

class JSONAttribute(object):
    def _assert_attr_class(self, var, cls):
        if not isinstance(var, cls):
            raise JSONAttributeError(
                'El atributo %s no es del tipo %s' % (var,cls))

        def to_python(self, value):
            raise NotImplemented

        def decode_to_object(self, obj, attr_name, value):
            raise NotImplemented
        
class JSONStringAttribute(JSONAttribute):
    def default_value(self):
        return ''

    def to_python(self, value):
        self._assert_attr_class(value, basestring)
        return value

class JSONIntegerAttribute(JSONAttribute):
    def default_value(self):
        return None

    def to_python(self, value):
        self._assert_attr_class(value, int)
        return value

class JSONObjectAttribute(JSONAttribute):
    def __init__(self, obj_class):
        self.obj_class = obj_class

    def default_value(self):
        return None

    def to_python(self, value):
        o = self.obj_class()
        o.decode_dict(value)
        return o
    
class JSONListAttribute(JSONAttribute):
    def __init__(self, list_class):
        self.list_class = list_class

    def default_value(self):
        return None

    def to_python(self, value):
        self._assert_attr_class(value, list)

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


class JSONAttributes(UserDict):
    def assert_exists(self, attr_name):
        '''Obtiene un atributo json del objeto'''
        try:
            return self[attr_name]
        except NameError:
            raise JSONObjectError('El atributo %s no existe en el objeto' % attr_name)

    def assert_class(self, attr_name, attr_cls):
        '''Chequea el tipo del atributo.'''
        self.assert_exists(attr_name)

        if not isinstance(self[attr_name], attr_cls):
            raise JSONObjectError('El atributo %s no es un '
                    'atributo del tipo %s' % (attr_name, str(attr_cls)))

    def is_class(self, attr_name, attr_cls):
        return isinstance(self[attr_name], attr_cls)