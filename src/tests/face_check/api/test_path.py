from random import randint
from unittest import TestCase

from face_check.api import path


class Dummy(object):
    """
    Dummy object to play with functions
    """

    #: python attribute annotation, required python 3.6
    attr: int = randint(0, 1024)

    def __init__(self, foo, parent=None):
        self._foo = foo
        self.parent = parent

    def foo(self):
        return self.foo


class HelpersTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dummy_dict = {
            'sample': 'lorem ipsum',
            'foo': lambda: 10**2,
            'another_dict': {
                'value': 10
            }
        }
        cls.dummy_root = Dummy(13373)
        cls.dummy = Dummy(1337, parent=cls.dummy_root)
        super().setUpClass()

    def test_object_get(self):
        self.assertEqual(path._object_get(self.dummy, 'attr'), self.dummy.attr)
        self.assertEqual(path._object_get(self.dummy, 'foo'), self.dummy.foo())
        self.assertEqual(path._object_get(self.dummy, '_foo'), self.dummy._foo)

        #: non existent entry is bounded to None
        self.assertEqual(path._object_get(self.dummy, 'non_existent'), None)

        #: can't get nested objects, should use traverse instead
        self.assertEqual(path._object_get(self.dummy, 'parent.attr'), None)

    def test_dict_get(self):
        self.assertEqual(path._dict_get(self.dummy_dict, 'sample'),
                         self.dummy_dict['sample'])
        self.assertEqual(path._dict_get(self.dummy_dict, 'foo'),
                         self.dummy_dict['foo']())

        #: non existent entry is bounded to empty dict instead of None
        self.assertEqual(path._dict_get(self.dummy_dict, 'another_dict.value'),
                         {})
        self.assertEqual(path._dict_get(self.dummy_dict, 'non_existent'), {})

    def test_traverse_obj(self):
        self.assertEqual(
            path._traverse_object(self.dummy, 'parent.foo'),
            self.dummy.parent.foo()
        )

        #: test with different type of delimiter
        self.assertEqual(
            path._traverse_object(self.dummy, 'parent$$foo',
                                  delimiter='$$'),
            self.dummy.parent.foo()
        )

        self.assertEqual(
            path._traverse_object(self.dummy, 'root1.root2.root3.root4'),
            None
        )

    def test_traverse_dict(self):
        self.assertEqual(
            path._traverse_dict(self.dummy_dict, 'another_dict.value'),
            self.dummy_dict['another_dict']['value']
        )

        #: test with different type of delimiter
        self.assertEqual(
            path._traverse_dict(self.dummy_dict, 'another_dict__value',
                                delimiter='__'),
            self.dummy_dict['another_dict']['value']
        )

        self.assertEqual(
            path._traverse_dict(self.dummy_dict, 'root1.root2.root3.root4'),
            {}
        )

    def test_traverse(self):
        """
        Tests traverse dict and object like entries
        """
        self.assertEqual(path.traverse(self.dummy, 'foo'), self.dummy.foo()
        )
        self.assertEqual(path.traverse(self.dummy_dict, 'foo'),
                         self.dummy_dict['foo']())
