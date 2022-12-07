from .utils import InvalidDirectory

from abc import ABC, abstractmethod
import os
import sys


class FileFilterStrategy(ABC):
    def __init__(self, dir):
        self.dir = dir
        self.files = [os.path.join(self.dir, file) for file in os.listdir(self.dir)]

    def is_valid(self, file):
        return not os.path.isdir(file)

    def get_files(self):
        return list(filter(self.is_valid, self.files))
    
    
class JPGFilterStrategy(FileFilterStrategy):
    
    EXTENSIONS = ['.jpg', '.jpeg']
    
    def is_valid(self, file):
        path, extension = os.path.splitext(file)
        return extension.lower() in self.EXTENSIONS


class Directory(object):
    def __init__(self, directory, get_files_strategy: FileFilterStrategy = JPGFilterStrategy):
        ## TODO: Try...Except
        self.directory = directory
        self.is_valid()
        self.get_files_strategy = get_files_strategy(directory)
        self.files = self.get_files_strategy.get_files()
        self.sub_directory = None
        
    def is_valid(self):
        if not os.path.isdir(self.directory):
            raise InvalidDirectory("Provided path is not a valid directory!")
            
    def is_empty(self):
        return not len(self.files)
    
    def get_files(self):
        return self.files
        
    def get_number_of_files(self):
        return len(self.files)
    
    def get_list_of_tuples_temp(self):
        file_data_tuples = []
        for path in self.files:
            file_path = path
            img_dir = self.directory
            file_name = os.path.basename(file_path)
            f, file_extension = os.path.splitext(file_name)
            file_data_tuples.append((file_path, img_dir, file_name, file_extension))
        return file_data_tuples
    
    
