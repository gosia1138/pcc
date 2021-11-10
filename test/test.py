#!/usr/bin/env python3
import PIL
import os
import unittest
from io import StringIO
from unittest.mock import patch
from .context import *


class TestValidFilename(unittest.TestCase):

    def test_correct_name(self):
        '''Should return true when fed correct filename'''
        name = 'good-file_name1138'
        result = check_valid_filename(name)
        self.assertTrue(result)

    def test_prohibited_names(self):
        '''Should return false when fed bad filenames'''
        names = [
            'you.can.but.you.should.not',
            'spaces are not cool',
            '@b$olut&ly*not?!',
            '/justdont',
        ]
        result = [not check_valid_filename(filename) for filename in names]
        self.assertTrue(all(result))

    def test_empty_string(self):
        '''Empty string should return false'''
        name = ''
        result = check_valid_filename(name)
        self.assertFalse(result)

    def test_too_long_name(self):
        '''name over 255 should return false'''
        name = 'a' * 256
        result = check_valid_filename(name)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
