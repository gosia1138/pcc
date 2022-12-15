from .utils import InvalidDirectory
from .filter_strategies import FileFilterStrategy, JPGFilterStrategy
import os


class Directory(object):
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
    
    def get_list_of_tuples_temp(self):
        file_data_tuples = []
        for path in self.files:
            file_path = path
            img_dir = self.directory
            file_name = os.path.basename(file_path)
            f, file_extension = os.path.splitext(file_name)
            file_data_tuples.append((file_path, img_dir, file_name, file_extension, self.subdirectory))
        return file_data_tuples
    
    
