from dataclasses import dataclass, field
import os
from shutil import copyfile


@dataclass
class ObjectGroupingMixin(object):
    grouping_factors: list[str] = field(default_factory=list, init=False)
    place: str = None
    timespace: str = None
    
    def add_grouping_factors(self, grouping_factor):
        self.grouping_factors.extend(grouping_factor)

    def grouping_dir(self, subdirectory):
        '''returns a group subdirectory to which image should be copied'''
        grouping_dir = os.path.join(self.path.parent, subdirectory)
        for factor in self.grouping_factors:
            if factor == "unknown":
                break
            grouping_dir = os.path.join(grouping_dir, str(factor))
        return grouping_dir, self.path.name

    def make_copy(self, subdirectory):
        '''Copy file into provided directory'''
        destination_dir, file_name = self.grouping_dir(subdirectory)
        if not os.path.isdir(destination_dir):
            os.makedirs(destination_dir)
        destination = os.path.join(destination_dir, file_name)
        if self.path.absolute != destination:
            copyfile(self.path.absolute(), destination)


class DirectoryGroupingMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._grouping_strategy = None
    
    def set_grouping_strategy(self, grouping_strategy):
        self._grouping_strategy = grouping_strategy(self.files)

    def add_grouping_factors_to_files(self):
        self._grouping_strategy.add_grouping_factors()

    def copy_files(self):
        for file in self.files:
            file.make_copy(self.subdirectory)
