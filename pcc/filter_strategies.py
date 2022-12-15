from abc import ABC, abstractmethod
import os


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