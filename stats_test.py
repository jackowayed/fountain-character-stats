#!/usr/bin/env python3

from stats import *
import unittest

class TestUtilityFunctions(unittest.TestCase):
    def test_is_character_name(self):
        self.assertTrue(is_character_name("JOHN"))
        self.assertTrue(is_character_name("JOHN SMITH"))
        # TODO reenable
        #self.assertTrue(is_character_name("JOHN SMITH (Hello 1.)"))

        self.assertFalse(is_character_name("John"))
        self.assertFalse(is_character_name("JOHN Smith"))
        self.assertFalse(is_character_name("JOHN   SMITH"))

if __name__ == '__main__':
    unittest.main()
