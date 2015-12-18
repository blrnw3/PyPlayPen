"""
:created: 10 Nov 2015
:author: bleerodgers
"""

import random
import unittest
from hash_map import HashMap

class TestHashMap(unittest.TestCase):
    """
    Basic test suite for the HashMap class
    """

    def test_construct(self):
        h = HashMap()

    def test_set_get_ok(self):
        h = HashMap()
        h.set('a', 5)
        self.assertEquals(h.get('a'), 5)

    def test_set_delete_get_err(self):
        h = HashMap()
        h.set('a', 5)
        h.delete('a')
        self.assertRaises(KeyError, h.get, 'a')

    def test_get_empty_err(self):
        h = HashMap()
        self.assertRaises(KeyError, h.get, 'a')

    def test_delete_empty_err(self):
        h = HashMap()
        self.assertRaises(KeyError, h.delete, 'a')

    def test_set_None_err(self):
        h = HashMap()
        self.assertRaises(ValueError, h.set, None, 5)

    def test_override_key(self):
        h = HashMap()
        h.set(1, 1)
        h.set(1, 2)
        self.assertEquals(h.get(1), 2)

    def test_resizing(self):
        h = HashMap()
        for i in xrange(h.INITIAL_CAPACITY * 2):
            h.set(i * i, i)

        for i in xrange(h.INITIAL_CAPACITY * 2):
            self.assertEquals(h.get(i * i), i)

    def test_collision_set(self):
        h = HashMap()
        size = h.INITIAL_CAPACITY
        h.set(size, 1)
        h.set(size * 2, 2)
        self.assertEquals(h.get(size), 1)
        self.assertEquals(h.get(size * 2), 2)

    def test_collision_delete(self):
        """
        Replicate a scenario whereby multiple keys with the same index are stored,
        then one in the middle is deleted, and the one at the end is accessed (get)
        IF the middle one was deleted completely, the get would fail
        BUT using a 'mark-as-deleted' strategy, it should work fine
        """
        h = HashMap()
        size = h.INITIAL_CAPACITY
        # These all have the same index after hashing since hash(n) == n
        h.set(size, 1)
        h.set(size * 2, 2)
        h.set(size * 3, 3)
        # Delete the 'middle' one
        h.delete(size * 2)
        # Get the 'last' one
        self.assertEquals(h.get(size * 3), 3)

    def test_brute_random_set_get_delete_get(self):
        h = HashMap()
        keys = [random.random() for i in xrange(1000)]
        for key in keys:
            h.set(key, key)

        for key in keys:
            self.assertEquals(h.get(key), key)

        for key in keys:
            h.delete(key)
            self.assertRaises(KeyError, h.get, key)
