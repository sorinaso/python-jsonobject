from json import loads
from attributes import *
from utils import JSONObjectError

class JSONObjectDecoder(object):
    def decode_dict(self, a_dict):
        '''Decodifica el diccionario sacado a partir de json
        al objeto.'''
        for k,v in self._json_attrs.items():
            v.decode_to_object(self, k, a_dict[k])

    def decode(self, json):
        '''Decodifica un json al objeto.'''
        self.decode_dict(loads(json))