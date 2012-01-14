import unittest
from attributes import JSONStringAttribute, JSONIntegerAttribute, JSONAttributeError, JSONBooleanAttribute
from jsonobject import JSONObject

class TestJSONAttributes(unittest.TestCase):
    def test_int(self):
        class TestObj(JSONObject):
            integer = JSONIntegerAttribute()

        o = TestObj()
        self.assertRaises(JSONAttributeError, o.encode)
        o.integer = 'test'
        self.assertRaises(JSONAttributeError, o.encode)
        o.integer = 4
        o.encode()

        self.assertRaises(JSONAttributeError, o.decode,'{ "integer": null }')
        self.assertRaises(JSONAttributeError, o.decode,'{ "integer": "test" }')
        o.decode('{ "integer": 4 }')

        class TestObj(JSONObject):
            integer = JSONIntegerAttribute(null=True)

        o = TestObj()
        o.decode('{ "integer": null }')
        self.assertRaises(JSONAttributeError, o.decode,'{ "integer": "test" }')
        o.decode('{ "integer": 4 }')
        
    def test_bool(self):
        class TestObj(JSONObject):
            boolean = JSONBooleanAttribute()

        o = TestObj()
        self.assertRaises(JSONAttributeError, o.encode)
        o.boolean = 'True'
        self.assertRaises(JSONAttributeError, o.encode)
        o.boolean = True; o.encode()
        o.boolean = False; o.encode()

        self.assertRaises(JSONAttributeError, o.decode,'{ "boolean": null }')
        self.assertRaises(JSONAttributeError, o.decode,'{ "boolean": "test" }')
        o.decode('{ "boolean": false }')

        class TestObj(JSONObject):
            boolean = JSONBooleanAttribute(null=True)

        o = TestObj()
        o.decode('{ "boolean": null }')
        self.assertRaises(JSONAttributeError, o.decode,'{ "boolean": "test" }')
        o.decode('{ "boolean": true }')

    def test_str(self):
        class TestObj(JSONObject):
            string = JSONStringAttribute()

        o = TestObj()
        o.encode()
        self.assertRaises(JSONAttributeError, o.decode,'{ "string": null }')
        self.assertRaises(JSONAttributeError, o.decode,'{ "string": 4 }')
        o.decode('{ "string": "lala" }')

        class TestObj(JSONObject):
            string = JSONStringAttribute(null=True)

        o = TestObj()
        o.decode('{ "string": null }')
        self.assertRaises(JSONAttributeError, o.decode,'{ "string": 4 }')
        o.decode('{ "string": "test" }')

if __name__ == '__main__':
    unittest.main()