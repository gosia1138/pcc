#!/usr/bin/env python3
import PIL
import os
import unittest
from io import StringIO
from unittest.mock import patch
from .context import *

class TestCheckParams(unittest.TestCase):

    def test_wrong_path(self):
        '''Returns false when passed non-existent path'''
        data = ("/non/existent/path", 500)
        result = check_params(*data)
        self.assertFalse(result)

    def test_wrong_size(self):
        '''Returns false when passed string as max_size'''
        data = (".", "non digit input")
        result = check_params(*data)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
