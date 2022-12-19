from abc import ABC, abstractmethod
from .grouping_utils import Place, Timespace

class GroupingStrategy(ABC):
    
    def __init__(self, files):
        self.files = files
    
    @abstractmethod
    def get_grouping_factors(self, file):
        pass

    def add_grouping_factors(self):
        for file in self.files:
            if grouping_factors := self.get_grouping_factors(file):
                file.add_grouping_factors(grouping_factors)


class YearGroupingStrategy(GroupingStrategy):
    def get_grouping_factors(self, file):
        return (str(file.created.year),)


class MonthGroupingStrategy(GroupingStrategy):
    def get_grouping_factors(self, file):
        return (str(file.created.strftime("%B")),)


class YearMonthGroupingStrategy(GroupingStrategy):
    def get_grouping_factors(self, file):
        return (str(file.created.year), file.created.strftime("%B"))


class PlaceGroupingStrategy(GroupingStrategy):
    def get_grouping_factors(self, file):
        if not getattr(file, "place", None):
            Place(file, self.files)
        return (getattr(file.place, "name", "unknown"),)


class TimePlaceGroupingStrategy(GroupingStrategy):
    def get_grouping_factors(self, file):
        if not getattr(file, "place", None):
            Place(file, self.files)
        if file.place == "unknown":
            file.timespace = "unknown"
        else:
            if not getattr(file, "timespace", None):
                Timespace(file, self.files)
            if not file.place == "unknown":
                return (file.timespace.getname(),)
            return
