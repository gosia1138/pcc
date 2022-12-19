from dataclasses import dataclass, field
import os
from datetime import datetime, timedelta
from math import acos, sin, cos, radians
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


class Place():
    counter = 0

    def __init__(self, img, images):
        self.id = Place.counter
        Place.counter += 1
        self.name = str(self.id)
        self.check_images(img, images)

    def check_images(self, img_1, images):
        '''Go through all other images and check if they can be assigned this Place'''
        for img_2 in images:
            if not getattr(img_2, "place", None):
                if self.get_distance(img_1, img_2) <= 10000:  # DISTANCE IN METERS
                    img_2.place = self

    def get_distance(self, img_1, img_2):
        '''Calculate geographical distance (in meters) between two images'''
        if not getattr(img_1, "coords", None) or not getattr(img_2, "coords", None):
            return -1
        lat1, long1 = map(radians, img_1.coords)
        lat2, long2 = map(radians, img_2.coords)
        d_long = abs(long1 - long2)
        if (lat1, long1) == (lat2, long2):
            return 0  # else acos may end up > 1 and throw error
        R = 6371000  # Appx. Earth radius in meters
        # Spherical Law of Cosines formula
        dist = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(d_long)) * R
        return dist



class Timespace():
    '''time span object to separate photos from the same place some time apart'''

    def __init__(self, img_src, images):
        self.place = img_src.place
        self.check_images(img_src, images)
        img_src.timespace = self

    def check_images(self, img_src, images):
        '''checks all the images if they can be assigned to this timespace
        if so updates self start/end and assigns itself to given image'''
        starts = img_src.created
        ends = img_src.created
        for img in images:
            if img.place == self.place:
                if img.created >= starts and img.created <= ends:
                    img.timespace = self
                elif img.created >= starts - timedelta(days=3) and img.created < starts:
                    starts = img.created
                    img.timespace = self
                elif img.created <= ends + timedelta(days=3) and img.created > ends:
                    ends = img.created
                    img.timespace = self
        self.starts = starts
        self.ends = ends

    def getname(self):
        '''returns name string consisting of place and start - end dates'''
        sd, sm, sy = self.starts.strftime("%d %b %y").split()
        ed, em, ey = self.ends.strftime("%d %b %y").split()
        if sy == ey:
            if sm == em:
                if sd == ed:
                    date = ed + em + ey
                else:
                    date = sd + "-" + ed + em + ey
            else:
                date = sd + sm + "-" + ed + em + ey
        else:
            date = sd + sm + sy + "-" + ed + em + ey
        name = self.place.name + "_" + date
        return name