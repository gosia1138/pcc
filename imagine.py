#!/usr/bin/env python3

import os
import sys
from datetime import datetime
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
        self.grouping_factor = ""

    def grouping_dir(self):
        '''returns a group subdirectory to which Image should be copied'''
        grouping_dir = os.path.join(self.dir, "imagine_output", self.grouping_factor)
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

    def make_copy(self):
        destination = os.path.join(*self.grouping_dir())
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


def group_images(images, factor):
    '''Add a grouping factor to each instance of ImageMeta'''
    for img in images:
        grouping_factor = getattr(img.created, "{}".format(factor))
        img.grouping_factor = str(grouping_factor)
        grouping_dir, file_name = img.grouping_dir()
        if not os.path.isdir(grouping_dir):
            os.makedirs(grouping_dir)
        img.make_copy()


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
    }
    print("\nThere are {} images in {}".format(len(source_list), img_dir))
    print("Here is what you can do with them:")
    print("[1] Group by year")
    print("[2] Group by month")
    print("[q] Quit")
    while True:
        users_choice = input("> ")
        if users_choice in actions.keys():
            group_images(images, actions[users_choice])
            for img in images:
                print(img.grouping_factor)
                print(img.grouping_dir())
            break
        elif users_choice.lower() == "q":
            sys.exit("Goodbye!")
        else:
            print("Invalid input, try again.")


if __name__ == '__main__':
    main()
