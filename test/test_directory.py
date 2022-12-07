from ..pcc.directory import Directory, FileFilterStrategy, JPGFilterStrategy
from ..pcc.utils import InvalidDirectory

import os
import pytest

test_dir = os.path.join(os.getcwd(), 'test', 'test_files')
invalid_test_dir = os.path.join(test_dir, 'this_is_not_jpg')

def test_if_directory_filters_correct_files_when_using_file_filter_startegy():
    directory = Directory(test_dir, FileFilterStrategy)
    assert directory.get_number_of_files() == 8

def test_if_directory_filters_correct_files_when_using_jpg_filter_startegy():
    directory = Directory(test_dir, JPGFilterStrategy)
    assert directory.get_number_of_files() == 7

def test_if_directory_raises_exception_if_fed_invalid_path():
    with pytest.raises(InvalidDirectory):
        directory = Directory(invalid_test_dir)


