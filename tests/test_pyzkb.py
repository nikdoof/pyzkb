#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyzkb
----------------------------------

Tests for `pyzkb` module.
"""

import unittest

from pyzkb import ZKillboard, InvalidModifier


class TestZKillboard(unittest.TestCase):

    def setUp(self):
        self.kb = ZKillboard()
        self.kb_noverification = ZKillboard(modifier_validation=False)

    def test_single_kill(self):
        headers, data = self.kb.get(killID=40403014)
        self.assertFalse(data == None)
        self.assertTrue(isinstance(data, list))
        self.assertTrue(isinstance(data[0], dict))
        self.assertTrue(len(data) == 1)
        self.assertTrue('killID' in data[0])

    def test_invalid_modifier(self):
        self.assertRaises(InvalidModifier, self.kb.blah)

    def test_invalid_parameter_modifier(self):
        self.assertRaises(InvalidModifier, self.kb.solo, 1)

    def test_no_parameter_modifier(self):
        self.assertRaises(InvalidModifier, self.kb.killID)

    def test_too_many_ids(self):
        self.assertRaises(ValueError, self.kb.solarSystemID, [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 11])

    def test_disabled_modifier_validation(self):
        try:
            self.kb_noverification.blah()
        except InvalidModifier:
            self.fail('Raise InvalidModifier unexpectedly.')

    def test_disabled_modifier_validation_parameter(self):
        try:
            self.kb_noverification.blah(213123)
        except InvalidModifier:
            self.fail('Raise InvalidModifier unexpectedly.')

    def test_no_writeback(self):
        x = self.kb.killID(40403014)
        self.assertTrue(len(self.kb._modifiers) == 0)
        self.assertTrue(len(x._modifiers) == 1)

    def test_xml_format_set(self):
        x = self.kb.xml()
        self.assertTrue(len(x._modifiers), 1)
        self.assertTrue(x._xml_format)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()