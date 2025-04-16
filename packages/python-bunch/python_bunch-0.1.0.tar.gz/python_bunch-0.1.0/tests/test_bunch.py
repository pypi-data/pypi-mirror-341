import unittest
from bunch.bunch import Bunch

class TestBunch(unittest.TestCase):
    def test_init(self):
        b = Bunch(name='Alice', age=30)
        self.assertEqual(b.name, 'Alice')
        self.assertEqual(b.age, 30)

    def test_getitem(self):
        b = Bunch(name='Alice', age=30)
        self.assertEqual(b['name'], 'Alice')

    def test_setitem(self):
        b = Bunch(name='Alice')
        b['age'] = 30
        self.assertEqual(b.age, 30)

    def test_contains(self):
        b = Bunch(name='Alice', age=30)
        self.assertTrue('name' in b)
        self.assertFalse('location' in b)

    def test_contains_value(self):
        b = Bunch(name='Alice', age=30)
        self.assertTrue(b.contains_value('Alice'))
        self.assertFalse(b.contains_value('Bob'))

    def test_from_dict(self):
        # Test from_dict static method
        data = {'fruit': 'apple', 'color': 'red'}
        b = Bunch.from_dict(data)
        self.assertEqual(b.fruit, 'apple')
        self.assertEqual(b.color, 'red')

if __name__ == '__main__':
    unittest.main()
