import os
from shutil import copyfile
from dataclasses import dataclass, field
from .utils import get_coordinates_from_exif_data, get_exif_data, get_datetime_from_exif_data
from typing import Any
from datetime import datetime
from pathlib import Path

@dataclass
class AnyFile:
    path: Path
    # TODO: move to Directory
    subdir: str


@dataclass
class JPGFile(AnyFile):
    place: str = field(init=False)
    created: datetime = field(init=False)
    exif_data: dict = field(default_factory=dict, init=False)
    coords: Any = field(init=False)
    grouping_factors: list[str] = field(default_factory=list, init=False)
  
    def __post_init__(self):
        self.exif_data = get_exif_data(self.path.absolute())
        if self.exif_data:
            self.coords = get_coordinates_from_exif_data(self.exif_data)
            self.created = get_datetime_from_exif_data(self.path.absolute(), self.exif_data)
        # TODO move to Place assigning function
        if not self.coords:                 
            self.place = "unknown"

    def grouping_dir(self):
        '''returns a group subdirectory to which image should be copied'''
        grouping_dir = os.path.join(self.path.parent, self.subdir)
        for factor in self.grouping_factors:
            if factor == "unknown":
                break
            grouping_dir = os.path.join(grouping_dir, str(factor))
        return grouping_dir, self.path.name

    def make_copy(self):
        '''Copy file into provided directory'''
        destination_dir, file_name = self.grouping_dir()
        if not os.path.isdir(destination_dir):
            os.makedirs(destination_dir)
        destination = os.path.join(destination_dir, file_name)
        if self.path.absolute != destination:
            copyfile(self.path.absolute(), destination)
