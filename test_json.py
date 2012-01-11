import json
import unittest
from jsonobject import JSONObject, JSONStringAttribute, JSONListAttribute, JSONObjectAttribute

class TestObj(JSONObject):
    field1 = JSONStringAttribute()
    
class TestInnerInner(JSONObject):
    field1 = JSONStringAttribute()
    field2 = JSONStringAttribute()

class TestInner(JSONObject):
    field1 = JSONStringAttribute()

    list2 = JSONListAttribute(list_class=TestInnerInner)
    
class TestOuter(JSONObject):
    field1 = JSONStringAttribute()
    field2 = JSONStringAttribute()

    list1 = JSONListAttribute(list_class=TestInner)
    obj1 = JSONObjectAttribute(obj_class=TestObj)

class TestJSON(unittest.TestCase):
    def test_metaclass(self):
        o = TestOuter()
        self.assertEqual(o.field1, '')
        self.assertIsInstance(o.field1, str)
        self.assertIsInstance(o._json_attrs['field1'], JSONStringAttribute)

        self.assertEqual(o.field2, '')
        self.assertIsInstance(o.field2, str)
        self.assertIsInstance(o._json_attrs['field2'], JSONStringAttribute)

        self.assertIs(o.list1, None)
        self.assertIsInstance(o._json_attrs['list1'], JSONListAttribute)

        self.assertIs(o.obj1, None)
        self.assertIsInstance(o._json_attrs['obj1'], JSONObjectAttribute)

    def test_decode(self):
        '''Testeo de logica de json'''
        json_str = '''{
            "field1": "o.field1",
            "field2": "o.field2",
            "list1":
            [{
                "field1": "o.list1[0].field1",
                "list2":
                [{
                    "field1": "o.list1[0].list2[0].field1",
                    "field2": "o.list1[0].list2[0].field2"
                },
                {
                    "field1": "o.list1[0].list2[1].field1",
                    "field2": "o.list1[0].list2[1].field2"
                }]
            }],
            "obj1": {
                "field1": "o.obj1.field1"
            }
        }'''

        o = TestOuter()
        o.decode(json_str)
        self._assert_decode(o)
        encoded_json = o.encode()

        o2 = TestOuter()
        o2.decode(encoded_json)
        self._assert_decode(o2)
        
    def _assert_decode(self, o):
        self.assertEqual(o.field1, 'o.field1')
        self.assertEqual(o.field2, 'o.field2')
        self.assertEqual(o.list1[0].field1, "o.list1[0].field1")
        self.assertEqual(o.list1[0].list2[0].field1, "o.list1[0].list2[0].field1")
        self.assertEqual(o.list1[0].list2[0].field2, "o.list1[0].list2[0].field2")
        self.assertEqual(o.list1[0].list2[1].field1, "o.list1[0].list2[1].field1")
        self.assertEqual(o.list1[0].list2[1].field1, "o.list1[0].list2[1].field1")
        self.assertEqual(o.obj1.field1, 'o.obj1.field1')

if __name__ == '__main__':
    unittest.main()