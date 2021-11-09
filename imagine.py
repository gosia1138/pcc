#!/usr/bin/env python3
import os
import re
import shutil
import sys
from tkinter import *
from tkinter import filedialog, ttk
from PIL import Image


def check_params(dir, max_size):
    '''Making sure directory exists and size entered is valid'''
    if not os.path.isdir(dir):
        print("Directory entered is not valid!")
        return False
    if not max_size.isdigit():
        print("Max size must be an integer!")
        return False
    return True


def check_valid_image(dir):
    '''Checking if the file is a valid image file that can be resized'''
    accepted_extensions = ('jpg', 'jpeg', 'png', 'gif', 'bmp')
    if os.path.isdir(dir):
        return False
    if not dir.lower().endswith(accepted_extensions):
        return False
    return True


def check_valid_filename(filename):
    '''Checking validity of constructed filenames'''
    valid_pattern = re.match(r'^[a-zA-Z0-9_-]+$', filename)
    valid_length = len(filename) < 256
    if valid_pattern and valid_length:
        return True
    return False


def resize_images(dir, max_size):
    '''getting content of chosen directory, opening it one by one and resizing'''
    files = os.listdir(dir)
    size = max_size, max_size
    thumbnails_dir = create_new_subdir(dir, "{}px_".format(str(max_size)))
    for file in files:
        file_dir = os.path.join(dir, file)
        if not check_valid_image(file_dir):
            continue
        with Image.open(file_dir) as im:
            if im.size[0] > max_size or im.size[1] > max_size:
                im.thumbnail(size)
            print("{:<20} - {} x {} pixels".format(file, im.size[0], im.size[1]))
            exif = im.info.get("exif", b'')
            os.chdir(thumbnails_dir)
            im.save(file, "JPEG", exif=exif)


def rename_images(dir, name_pattern):
    '''renaming images with proposed pattern followed by incrementing numbers'''
    files = os.listdir(dir)
    renamed_files_dir = create_new_subdir(dir, name_pattern)
    file_count = 0
    for file in files:
        src = os.path.join(dir, file)
        if not check_valid_image(src):
            continue
        filename, file_extension = os.path.splitext(src)
        new_name = name_pattern + str(file_count) + file_extension
        dst = os.path.join(renamed_files_dir, new_name)
        shutil.copy2(src, dst)
        file_count += 1


def create_new_subdir(dir, name):
    '''Creating subdirectory inside images directory to store resized images'''
    subdir_count = 0
    while os.path.isdir(os.path.join(dir, "{}{}".format(name, str(subdir_count)))):
        subdir_count += 1
    path = os.path.join(dir, "{}{}".format(name, str(subdir_count)))
    os.mkdir(path)
    return path


def initialize_gui():
    '''Initializing Imagine class with root as a parent -- GUI'''
    root = Tk()
    Imagine(root)
    root.mainloop()

class Imagine:
    '''Dialog window class Tkinter'''

    def __init__(self, root):
        self.root = root

        root.title("Imagine - bulk image manipulator")
        # Creating the main frame
        mainframe = ttk.Frame(root, padding=10)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # creating the widget with mainframe as a parent - image directory
        ttk.Label(mainframe, text="Enter images directory:").grid(column=0, columnspan=4, row=0, sticky=W)
        self.images_dir = StringVar()
        images_dir_entry = ttk.Entry(mainframe, width=40, textvariable=self.images_dir)
        images_dir_entry.grid(column=0, row=1, columnspan=4, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.images_dir).grid(column=0, columnspan=4, row=2, sticky=(W, E))

        # enter maximum size of images
        ttk.Label(mainframe, text="Enter maximum size in pixels: ").grid(column=0, columnspan=3, row=3, sticky=W)
        self.max_size = StringVar()
        max_size_entry = ttk.Entry(mainframe, width=10, textvariable=self.max_size)
        max_size_entry.grid(column=3, row=3, sticky=(W, E))

        # OK and cancel buttons
        ttk.Button(mainframe, text="OK", command=self.finalize).grid(column=2, row=4, sticky=W)
        ttk.Button(mainframe, text="Cancel", command=lambda : root.destroy()).grid(column=3, row=4, sticky=W)

        # Adding aditional padding and focusing coursor in dialog box
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        images_dir_entry.focus()
        root.bind("<Return>", self.finalize) # Binding hitting enter with check_params() function

    def finalize(self, *args):
        '''Checking parameters, passing to actual resizing function and killing the GUI'''
        image_dir = self.images_dir.get()
        max_size = self.max_size.get()
        if check_params(image_dir, max_size):
            self.root.destroy() # Killing the dialog window
            resize_images(image_dir, int(max_size))
        print(image_dir, max_size)

def main():
    '''Checking for command line arguments to pass to resizing function'''
    if len(sys.argv) == 4:
        image_dir = sys.argv[2]
        if sys.argv[1].lower() == '--resize':
            max_size = sys.argv[3]
            if check_params(image_dir, max_size):
                resize_images(image_dir, int(max_size))
        elif sys.argv[1].lower() == '--rename':
            new_name = sys.argv[3]
            rename_images(image_dir, new_name)

        else:
            print('''
                To use command line input use following pattern:
                FOR RESIZING:
                $ ./imagine --resize <images directory> <maximum size>
                FOR RENAMING:
                $ ./imagine --rename <images directory> <name pattern>
            ''')
            initialize_gui()
    else:
        initialize_gui()


if __name__ == '__main__':
    main()
