from dataclasses import dataclass
from math import acos, sin, cos, radians
import os
import requests


@dataclass
class GeographicalCoordinates:
    latitude: float
    longitude: float 

    def get_distance_from(self, coordinates: 'GeographicalCoordinates'):
        lat1, long1 = map(radians, (self.latitude, self.longitude))
        lat2, long2 = map(radians, (coordinates.latitude, coordinates.longitude))
        d_long = abs(long1 - long2)
        if (lat1, long1) == (lat2, long2):
            return 0  # else acos may end up > 1 and throw error
        R = 6371000  # Appx. Earth radius in meters
        # Spherical Law of Cosines formula
        distance = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(d_long)) * R
        return distance

    def is_in_vicinity(self, coordinates, max_distance):
        return self.get_distance_from(coordinates) <= max_distance

    def get_coordinates_as_str(self):
        return f"{self.latitude}_{self.longitude}"


def get_address_dict_from_api(coords: GeographicalCoordinates):
    api_endpoint = os.environ.get('LOCATIONIQ_ENDPOINT_URL')
    api_key = os.environ.get('LOCATIONIQ_API_KEY')
    lat = coords.latitude
    lon = coords.longitude
    zoom = 15
    if api_endpoint and api_key:   
        response = requests.get(f'{api_endpoint}/v1/reverse.php?key={api_key}&lat={lat}&lon={lon}&zoom={zoom}&format=json')
        address_dict = response.json().get('address', {})   
    return address_dict
