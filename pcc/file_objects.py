from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
from shutil import copyfile


class JPGFile():
    def __init__(self, full_path, directory, filename, extension, subdir):
        '''extract file info from path and collect other data from exif'''
        # image data
        self.path = full_path
        self.dir = directory
        self.name = filename
        self.type = extension
        self.subdir = subdir
        self.extract_data()
        self.get_datetime()
        if not getattr(self, "coords", None):
            self.place = "unknown"
        # grouping data
        self.grouping_factors = []

    def extract_data(self):
        '''extracting image exif and size data'''
        exif_data = {}
        with Image.open(self.path) as im:
            info = im._getexif()
            self.size = im.size
        if info:
            for tag, value in info.items():  # decoding exif data
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}  # creating a sub-dictionary of gps info
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]
                    exif_data[decoded] = gps_data
                    if gps_data:  # creating attribute "coords" from EXIF GPS data
                        try:
                            lat_d, lat_m, lat_s = [int(value) for value in gps_data["GPSLatitude"]]
                            lat_sign = gps_data["GPSLatitudeRef"]
                            lat = (lat_d + lat_m/60 + lat_s/3600) * (1 - 2*(lat_sign == "S"))
                            long_d, long_m, long_s = [int(value) for value in gps_data["GPSLongitude"]]
                            long_sign = gps_data["GPSLongitudeRef"]
                            long = (long_d + long_m/60 + long_s/3600) * (1 - 2*(long_sign == "W"))
                            self.coords = (lat, long)
                        except Exception:
                            pass
                else:
                    exif_data[decoded] = value
        self.exif = exif_data

    def get_datetime(self):
        '''Try to get creation date from exif or fallback to ctime. Return a datetime object'''
        created = datetime.fromtimestamp(os.path.getctime(self.path))
        datetime_str = self.exif.get("DateTime", None)
        if datetime_str:
            created = datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S")
        self.created = created

    def grouping_dir(self):
        '''returns a group subdirectory to which image should be copied'''
        grouping_dir = os.path.join(self.dir, self.subdir)
        for factor in self.grouping_factors:
            if factor == "unknown":
                break
            grouping_dir = os.path.join(grouping_dir, str(factor))
        return grouping_dir, self.name

    def make_copy(self):
        '''Copy image into provided directory'''
        destination_dir, file_name = self.grouping_dir()
        if not os.path.isdir(destination_dir):
            os.makedirs(destination_dir)
        destination = os.path.join(destination_dir, file_name)
        if self.path != destination:
            copyfile(self.path, destination)
