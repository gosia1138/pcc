from ..file_objects import JPGFile
from datetime import datetime, timedelta
from .coordinates import get_address_dict_from_api
import pprint
from .utils import get_valid_filename

class Place():

    def __init__(self, img: JPGFile, images: list):
        self.coords = img.coords
        self.address_dict = get_address_dict_from_api(self.coords)
        self.images_to_check = images
        self.get_user_input()
        self.check_images()

    def display_geographical_information(self):
        print(self.coords.get_coordinates_as_str())
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.address_dict)

    def get_user_input(self):
        self.display_geographical_information()
        self.name = get_valid_filename(input("How do we name this place? (leave blank to ignore)\n>"))
        while True:
            try:
                self.max_radius = int(input("How far away photos should be included in that place? [km]\n>") or 0) * 1000
                break
            except ValueError:
                print("Please provide a valid integer!")

    def check_images(self):
        '''Go through all other images and check if they can be assigned this Place'''
        for image in self.images_to_check:
            if not getattr(image, "place", None):
                if self.coords.is_in_vicinity(image.coords, self.max_radius):
                    image.place = self

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
        # TODO allow user input as with distances
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