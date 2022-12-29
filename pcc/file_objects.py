from dataclasses import dataclass, field
from .utils.exif_utils import (
    get_coordinates_from_exif_data,
    get_exif_data,
    get_datetime_from_exif_data)
from .utils.mixins import ObjectGroupingMixin
from typing import Any
from datetime import datetime
from pathlib import Path
import os


@dataclass
class AnyFile:
    path: Path
    created: datetime = field(init=False)
    
    def __post_init__(self):
        self.created = datetime.fromtimestamp(os.path.getctime(self.path))


@dataclass
class JPGFile(ObjectGroupingMixin, AnyFile):
    place: str = field(init=False)
    exif_data: dict = field(default_factory=dict, init=False)
    coords: Any = field(init=False, default=None)
    grouping_factors: list[str] = field(default_factory=list, init=False)
  
    def __post_init__(self):
        super().__post_init__()
        self.exif_data = get_exif_data(self.path.absolute())
        if self.exif_data:
            self.coords = get_coordinates_from_exif_data(self.exif_data)
            exif_created = get_datetime_from_exif_data(self.exif_data)
            if exif_created:
                self.created = exif_created
        # TODO move to Place assigning function
        if not self.coords:                 
            self.place = "unknown"
