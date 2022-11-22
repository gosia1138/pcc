from abc import ABC, abstractmethod
import os
import sys


class GetFilesStrategy(object):
    def __init__(self, directory):
        self.directory = directory
        
    def get_files(self):
        filenames = os.listdir(self.directory)
        files = [os.path.join(self.directory, filename) for filename in filenames if not os.path.isdir(filename)]
        return files
    
    
class GetJPGFilesStrategy(GetFilesStrategy):
    
    EXTENSIONS = ['.jpg', '.jpeg']
    
    def is_valid(self, file):
        path, extension = os.path.splitext(file)
        return extension.lower() in self.EXTENSIONS

    def get_files(self):
        all_files = super().get_files()
        jpg_files = list(filter(self.is_valid, all_files))
        return jpg_files
    

class Directory(object):
    def __init__(self, directory, get_files_strategy: GetFilesStrategy = GetFilesStrategy):
        ## TODO: Try...Except
        self.directory = directory
        self.is_valid()
        self.get_files_strategy = get_files_strategy(directory)
        self.files = self.get_files_strategy.get_files()
        self.sub_directory = None
        
    def is_valid(self):
        if not os.path.isdir(self.directory):
        ## TODO: raise Exception
            sys.exit("Entered directory is not valid!")
            
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
    
    
