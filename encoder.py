import json
from attributes import *

class JSONObjectEncoder(object):
    def build_dict(self):
        enc_dict = {}

        for k, v in self._json_attrs.items():
            a = getattr(self, k)
            if isinstance(v, JSONStringAttribute):
                enc_dict[k] = a
            elif isinstance(v, JSONObjectAttribute):
                enc_dict[k] = a.build_dict()
            elif isinstance(v, JSONListAttribute):
                enc_dict[k] = []
                for e in a:
                    enc_dict[k].append(e.build_dict())

        return enc_dict
    
    def encode(self):
        return json.dumps(self.build_dict())

