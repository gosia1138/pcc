from .utils import InvalidDirectory, DirectoryGroupingMixin
from .filter_strategies import FileFilterStrategy, JPGFilterStrategy
import os


class Directory(DirectoryGroupingMixin):
    def __init__(self, directory, get_files_strategy: FileFilterStrategy = JPGFilterStrategy):
        ## TODO: Try...Except
        self.directory = directory
        self.is_valid()
        self.get_files_strategy = get_files_strategy(directory)
        self.files = self.get_files_strategy.get_files()
        self.subdirectory = self.create_subdirectory()
        
    def is_valid(self):
        if not os.path.isdir(self.directory):
            raise InvalidDirectory("Provided path is not a valid directory!")
            
    def is_empty(self):
        return not len(self.files)
    
    def get_files(self):
        return self.files
        
    def get_number_of_files(self):
        return len(self.files)

    def create_subdirectory(self):
        '''Create unique imagine output directory each run'''
        n = 0
        while True:
            subdirectory = "imagine{}".format(str(n).zfill(2))
            abs_sub = os.path.join(self.directory, subdirectory)
            if not os.path.isdir(abs_sub):
                break
            n += 1
        return subdirectory
    