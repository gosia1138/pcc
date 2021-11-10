#!/usr/bin/env python3
import os
import re
import shutil
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def create_source_list(dir):
    '''Returning list of dictionaries representing images contained in the directory'''
    if not os.path.isdir(dir):
        sys.exit("Entered directory is not valid!")
    source = []
    files = os.listdir(dir)
    accepted_extensions = ('jpg', 'jpeg')
    for file in files:
        file_path = os.path.join(dir, file)
        if os.path.isdir(file_path):
            continue    # skip directories
        if not file.lower().endswith(accepted_extensions):
            continue    # skip files that do not have accepted extensions
        source.append({
                'file': file,
                'full_path': file_path,
                'dir': dir,
            })
    return source

def extract_exif(im):
    exif_data = {}
    info = im._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
    return exif_data


def check_valid_filename(filename):
    '''Checking validity of constructed filenames'''
    valid_pattern = re.match(r'^[a-zA-Z0-9_-]+$', filename)
    valid_length = len(filename) < 256
    if valid_pattern and valid_length:
        return True
    return False


def resize_images(source, max_size):
    '''getting paths of chosen directory, opening it one by one and resizing'''
    size = max_size, max_size
    thumbnails_dir = create_new_subdir(source[0]['dir'], "{}px_".format(str(max_size)))
    for image in source:
        with Image.open(image['full_path']) as im:
            if im.size[0] > max_size or im.size[1] > max_size:
                im.thumbnail(size)
            print("{:<20} - {} x {} pixels".format(image['file'], im.size[0], im.size[1]))
            exif_dict = extract_exif(im)
            os.chdir(thumbnails_dir)
            im.save(image['file'], "JPEG", exif=im.getexif())


def rename_images(source, name_pattern):
    '''renaming images with proposed pattern followed by incrementing numbers'''
    renamed_files_dir = create_new_subdir(source[0]['dir'], name_pattern)
    file_count = 0
    for image in source:
        filename, file_extension = os.path.splitext(image['file'])
        new_name = name_pattern + str(file_count) + file_extension
        destination = os.path.join(renamed_files_dir, new_name)
        shutil.copy2(image['full_path'], destination)
        file_count += 1


def create_new_subdir(dir, name):
    '''Creating subdirectory inside images directory to store resized images'''
    subdir_count = 0
    while os.path.isdir(os.path.join(dir, "{}{}".format(name, str(subdir_count)))):
        subdir_count += 1
    path = os.path.join(dir, "{}{}".format(name, str(subdir_count)))
    os.mkdir(path)
    return path


def main():
    # TEMPORARY CLI
    '''Checking for command line arguments to pass to resizing function'''
    if len(sys.argv) == 4:
        source_dir = create_source_list(sys.argv[2])
        # ------RESIZE------
        if sys.argv[1] in ('-R', '--resize'):
            max_size = sys.argv[3]
            if not max_size.isdigit():
                sys.exit("Size parameter must be an integer!")
            resize_images(source_dir, int(max_size))
        # ------RENAME------
        elif sys.argv[1] in ('-r', '--rename'):
            new_name = sys.argv[3]
            rename_images(source_dir, new_name)

    else:
        sys.exit('''
To use command line input use following pattern:

FOR RESIZING:
$ ./imagine --resize <images directory> <maximum size>

FOR RENAMING:
$ ./imagine --rename <images directory> <name pattern>''')


if __name__ == '__main__':
    main()
