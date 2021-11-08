#!/usr/bin/env python3
import os
import re
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

def resize_images(dir, max_size):
    '''getting content of chosen directory, opening it one by one and resizing'''
    files = os.listdir(dir)
    size = max_size, max_size
    thumbnails_dir = create_new_subdir(dir)
    for file in files:
        file_dir = os.path.join(dir, file)
        if os.path.isdir(file_dir):
            continue
        with Image.open(file_dir) as im:
            if im.size[0] > max_size or im.size[1] > max_size:
                im.thumbnail(size)
            print("{:<20} - {} x {} pixels".format(file, im.size[0], im.size[1]))
            os.chdir(thumbnails_dir)
            im.save(file, "JPEG")


def create_new_subdir(dir):
    '''Creating subdirectory inside images directory to store resized images'''
    subdir_count = 0
    while os.path.isdir(os.path.join(dir, "thumbnails{}".format(str(subdir_count)))):
        subdir_count += 1
    path = os.path.join(dir, "thumbnails{}".format(str(subdir_count)))
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
    if len(sys.argv) == 3:
        image_dir = sys.argv[1]
        max_size = sys.argv[2]
        if check_params(image_dir, max_size):
            resize_images(image_dir, int(max_size))
        else:
            print('''
                To use command line input use following pattern:
                $ imagine <images directory> <maximum size>
            ''')
            initialize_gui()
    else:
        initialize_gui()


if __name__ == '__main__':
    main()
