from abc import ABC, abstractmethod
import os
from pathlib import Path
from .file_objects import AnyFile, JPGFile


class FileFilterStrategy(ABC):
    def __init__(self, dir):
        self.dir = dir
        self.all_paths = [Path(os.path.join(self.dir, file)) for file in os.listdir(self.dir)]
        self.file_class = AnyFile

    def is_valid(self, path):
        return not path.is_dir()

    def get_valid_paths(self):
        return list(filter(self.is_valid, self.all_paths))

    def get_files(self):
        return list(map(self.file_class, self.get_valid_paths()))
    
    
class JPGFilterStrategy(FileFilterStrategy):
    
    EXTENSIONS = ['.jpg', '.jpeg']

    def __init__(self, dir):
        super().__init__(dir)
        self.file_class = JPGFile
    
    def is_valid(self, path):
        return path.suffix.lower() in self.EXTENSIONS