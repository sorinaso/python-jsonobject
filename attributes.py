from UserDict import UserDict
from utils import JSONObjectError

class JSONAttribute(object):
    pass

class JSONStringAttribute(JSONAttribute):
    def to_python(self):
        return ''

class JSONObjectAttribute(JSONAttribute):
    def __init__(self, obj_class):
        self.obj_class = obj_class

    def to_python(self):
        return None

class JSONListAttribute(JSONAttribute):
    def __init__(self, list_class):
        self.list_class = list_class

    def to_python(self):
        return None

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