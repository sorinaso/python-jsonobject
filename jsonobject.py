from attributes import *
from decoder import JSONObjectDecoder
from encoder import JSONObjectEncoder

class JSONObjectBuilder(type):
    """
    A metaclass to normalize arguments give to the get_db_prep_* and db_type
    methods on fields.
    """
    def __new__(cls, name, bases, attrs):
        new_cls = super(JSONObjectBuilder, cls).__new__(cls, name, bases, attrs)
        json_fields = JSONAttributes()
        
        for k,v in attrs.items():
            if isinstance(v, JSONAttribute):
                json_fields[k] = v
                setattr(new_cls, k, v.to_python())

        setattr(new_cls, '_json_attrs', json_fields)

        return new_cls


class JSONObject(JSONObjectEncoder, JSONObjectDecoder):
    __metaclass__ = JSONObjectBuilder