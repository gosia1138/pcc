#!/usr/bin/env python3
import os
import re
import shutil
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class ImageMeta():
    def __init__(self, file_path, file_name, file_extension):
        self.path = file_path
        self.name = file_name
        self.type = file_extension
        img_data = self.extract_data()
        self.exif = img_data[0]
        self.size = img_data[1]
        self.datetime = self.get_datetime()

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
        datetime_str = self.exif.get("DateTime", None)
        if datetime_str:
            pattern = r"(\d\d\d\d):(\d\d):(\d\d) (\d\d):(\d\d):(\d\d)"
            datetime = re.search(pattern, datetime_str)
            return datetime
        return None


def create_source_list(dir, valid_extensions):
    '''Returning list of tuples representing images contained in the directory'''
    if not os.path.isdir(dir):
        sys.exit("Entered directory is not valid!")
    source = []
    files = os.listdir(dir)
    for file_name in files:
        file_path = os.path.join(dir, file_name)
        file_dir, file_extension = os.path.splitext(file_path)
        if os.path.isdir(file_path):
            continue    # skip directories
        if file_extension.lower() not in valid_extensions:
            continue    # skip files that do not have accepted extensions
        source.append((file_path, file_name, file_extension))
    return source


def main():
    valid_extensions = ('.jpg', '.jpeg')
    if len(sys.argv) == 2:
        img_dir = sys.argv[1]
        source_list = create_source_list(img_dir, valid_extensions)
        images = [ImageMeta(*file_data) for file_data in source_list]

        for img in images:
            print(img.name)
            print(img.get_datetime())
    else:
        sys.exit("""Correct input: 'python3 imagine.py <images_directory>'""")


if __name__ == '__main__':
    main()
