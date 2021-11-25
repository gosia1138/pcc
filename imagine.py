#!/usr/bin/env python3

import os
import sys
from datetime import datetime
from math import acos, sin, cos, radians
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from shutil import copyfile


class ImageMeta():
    def __init__(self, file_path, file_dir, file_name, file_extension):
        '''extract file info from path and collect other data from exif'''
        # image data
        self.path = file_path
        self.dir = file_dir
        self.name = file_name
        self.type = file_extension
        self.exif, self.size = self.extract_data()
        self.created = self.get_datetime()
        # grouping data
        self.grouping_factors = []
        self.get_coords()

    def grouping_dir(self, sub_dir):
        '''returns a group subdirectory to which Image should be copied'''
        grouping_dir = os.path.join(self.dir, sub_dir)
        for factor in self.grouping_factors:
            grouping_dir = os.path.join(grouping_dir, factor)
        return grouping_dir, self.name

    def extract_data(self):
        '''extracting image exif and size data'''
        exif_data = {}
        with Image.open(self.path) as im:
            info = im._getexif()
            size = im.size
        if info:
            for tag, value in info.items():  # decoding exif data
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}  # creating a sub-dictionary of gps info
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]
                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value
        return exif_data, size

    def get_datetime(self):
        '''Try to get creation date from exif or fallback to ctime. Return a datetime object'''
        datetime_str = self.exif.get("DateTime", None)
        if datetime_str:
            created = datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S")
            return created
        else:  # get creation/modification time of the file
            ctime = datetime.fromtimestamp(os.path.getctime(self.path))
            return ctime

    def get_coords(self):
        GPSInfo = self.exif.get("GPSInfo", None)
        if GPSInfo:
            lat_d, lat_m, lat_s = [int(value) for value in GPSInfo["GPSLatitude"]]
            lat_sign = GPSInfo["GPSLatitudeRef"]
            lat = (lat_d + lat_m/60 + lat_s/3600) * (1 - 2*(lat_sign == "S"))
            long_d, long_m, long_s = [int(value) for value in GPSInfo["GPSLongitude"]]
            long_sign = GPSInfo["GPSLongitudeRef"]
            long = (long_d + long_m/60 + long_s/3600) * (1 - 2*(long_sign == "W"))
            self.coords = (lat, long)

    def make_copy(self, sub_dir):
        destination_dir, file_name = self.grouping_dir(sub_dir)
        if not os.path.isdir(destination_dir):
            os.makedirs(destination_dir)
        destination = os.path.join(destination_dir, file_name)
        if self.path != destination:
            copyfile(self.path, destination)


def create_source_list(img_dir, valid_extensions):
    '''Returning list of tuples representing images contained in the directory'''
    if not os.path.isdir(img_dir):
        sys.exit("Entered directory is not valid!")
    source = []
    files = os.listdir(img_dir)
    for file_name in files:
        file_path = os.path.join(img_dir, file_name)
        f, file_extension = os.path.splitext(file_path)
        if os.path.isdir(file_path):
            continue    # skip directories
        if file_extension.lower() not in valid_extensions:
            continue    # skip files that do not have accepted extensions
        source.append((file_path, img_dir, file_name, file_extension))
    return source


def add_grouping_factor(images, factor):
    '''Add a grouping factor to each instance of ImageMeta'''
    for img in images:
        # time factors
        if factor == "year":
            gf = (str(img.created.year), )
        elif factor == "month":
            gf = (img.created.strftime("%B"), )
        elif factor == ("year", "month"):
            gf = (str(img.created.year), img.created.strftime("%B"))
        img.grouping_factors += gf


def create_subdir(img_dir):
    '''Create unique imagine sub-directory each run'''
    n = 0
    while True:
        sub_dir = "imagine{}".format(str(n).zfill(2))
        abs_sub = os.path.join(img_dir, sub_dir)
        if not os.path.isdir(abs_sub):
            break
        n += 1
    return sub_dir


def get_distance(img_1, img_2):
    '''Calculate geographical distance (in meters) between two images'''
    if not getattr(img_1, "coords", None) or not getattr(img_2, "coords", None):
        return -1
    lat1, long1 = map(radians, img_1.coords)
    lat2, long2 = map(radians, img_2.coords)
    d_long = abs(long1 - long2)
    R = 6371000  # Appx. Earth radius in meters
    # Spherical Law of Cosines formula
    dist = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(d_long)) * R
    return dist


def main():
    # create list of ImageMeta classes from given directory
    valid_extensions = ('.jpg', '.jpeg')
    if len(sys.argv) == 2:
        img_dir = sys.argv[1]
        source_list = create_source_list(img_dir, valid_extensions)
        images = [ImageMeta(*file_data) for file_data in source_list]
    else:
        sys.exit("Correct input: 'python3 imagine.py <images_directory>'")

    # prompt user about action to be taken with the images
    actions = {
        "1": "year",
        "2": "month",
        "3": ("year", "month"),
    }
    print("\nThere are {} images in {}".format(len(source_list), img_dir))
    print("Here is what you can do with them:")
    print("[1] Group by year")
    print("[2] Group by month")
    print("[3] Group by year and month")
    print("[q] Quit")
    while True:
        users_choice = input("> ")
        if users_choice in actions.keys():
            add_grouping_factor(images, actions[users_choice])
            subdir = create_subdir(img_dir)
            for img in images:
                img.make_copy(subdir)
            break
        elif users_choice.lower() == "q":
            sys.exit("Goodbye!")
        else:
            print("Invalid input, try again.")


if __name__ == '__main__':
    main()
