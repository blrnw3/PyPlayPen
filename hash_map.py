"""
:created: 10 Nov 2015
:author: bleerodgers
"""

from collections import namedtuple

Entry = namedtuple('Entry', 'key val')


class HashMap(object):
    """
    Implementation of a Hash Map without using a dictionary

    Base structure is a standard python list
    Entries are stored as namedtuples of key-value pairs

    The collision strategy used is open addressing with linear probing
    For simplicity, keys of None are disallowed as they are used as 'dummy' entries
        so that probing skips over entries which have been deleted
    The hashmap doubles when it is 70% full to prevent performance degradation
    """

    INITIAL_CAPACITY = 8

    def __init__(self):
        self._data = [None] * self.INITIAL_CAPACITY
        self.size = self.INITIAL_CAPACITY
        self.active_count = 0

    def set(self, key, val):
        """ Add or override an entry """
        if key is None:
            raise ValueError('None is not a valid key for this data structure')

        slot_num = self._seek(key)
        self._data[slot_num] = Entry(key, val)

        self.active_count += 1
        if self.active_count / (1.0 * self.size) > 0.7:
            self._resize()

    def get(self, key):
        """ Get the value of an entry with the given key """
        slot_num = self._seek(key)

        if self._data[slot_num] is None:
            raise KeyError

        return self._data[slot_num].val

    def delete(self, key):
        """ Delete the entry with the given key"""
        slot_num = self._seek(key)

        if self._data[slot_num] is None:
            raise KeyError

        # Mark it as Deleted so linear probing still works
        # Replace entry completely to free up memory (could be storing large object)
        self._data[slot_num] = Entry(None, None)

        self.active_count -= 1

    def _resize(self):
        self.size *= 2
        old_data = self._data[:]
        self._data = [None] * self.size
        for item in old_data:
            if item is not None:
                self.set(item.key, item.val)

    def _seek(self, key):
        slot_num = hash(key) % self.size
        while self._data[slot_num] is not None and self._data[slot_num].key != key:
            slot_num = (slot_num + 1) % self.size
        return slot_num

    def __str__(self):
        return ', '.join('"%s": %s ' % (e.key, e.val) for e in self._data if e)

    def __repr__(self):
       return str(self._data)
