from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image
from datetime import datetime
import os
from .coordinates import GeographicalCoordinates

def get_raw_exif_data(path):
    try:
        with Image.open(path) as image:
            return image._getexif()
    except:
        print(f'Failed to extract EXIF data from {path}')
        return None

def get_exif_data(path):
    if raw_exif_data := get_raw_exif_data(path):
        decoded_exif_data = {}
        for tag, value in raw_exif_data.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                decoded_exif_data[decoded] = gps_data
            elif decoded:
                decoded_exif_data[decoded] = value
        return decoded_exif_data
    return None

def get_coordinates_from_exif_data(exif_data):
    gps_data = exif_data.get('GPSInfo', None)
    if gps_data:
        try:
            lat_d, lat_m, lat_s = [int(value) for value in gps_data["GPSLatitude"]]
            lat_sign = gps_data["GPSLatitudeRef"]
            lat = (lat_d + lat_m/60 + lat_s/3600) * (1 - 2*(lat_sign == "S"))
            long_d, long_m, long_s = [int(value) for value in gps_data["GPSLongitude"]]
            long_sign = gps_data["GPSLongitudeRef"]
            long = (long_d + long_m/60 + long_s/3600) * (1 - 2*(long_sign == "W"))
            return GeographicalCoordinates(lat, long)
        except Exception:
            pass
    return None

def get_datetime_from_exif_data(path, exif_data):
    created = datetime.fromtimestamp(os.path.getctime(path))
    datetime_str = exif_data.get("DateTime", None)
    if datetime_str:
        created = datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S")
    return created