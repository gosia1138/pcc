#!/usr/bin/env python3

import sys
from datetime import datetime, timedelta
from math import acos, sin, cos, radians
from operator import attrgetter
from pcc.directory import Directory, JPGFilterStrategy
from pcc.file_objects import JPGFile
from pcc.utils.grouping_strategies import (
    YearGroupingStrategy,
    MonthGroupingStrategy,
    YearMonthGroupingStrategy,
    PlaceGroupingStrategy,
    TimePlaceGroupingStrategy)


if __name__ == '__main__':
    # create list of JPGFile classes from given directory
    if len(sys.argv) == 2:
        directory = sys.argv[1]
        images_directory = Directory(directory, JPGFilterStrategy)
    else:
        sys.exit("Correct input: 'python3 imagine.py <images_directory>'")

    # prompt user about action to be taken with the images
    actions = {
        "1": YearGroupingStrategy,
        "2": MonthGroupingStrategy,
        "3": YearMonthGroupingStrategy,
        "4": PlaceGroupingStrategy,
        "5": TimePlaceGroupingStrategy
    }

    print(f"\nThere are {images_directory.get_number_of_files()} images in {images_directory.directory}")
    print("Here is what you can do with them:")
    print("[1] Group by year")
    print("[2] Group by month")
    print("[3] Group by year and month")
    print("[4] Group by places")
    print("[5] Smart Grouping (place and date)")
    print("[q] Quit")
    
    while True:
        users_choice = input("> ")
        if users_choice in actions.keys():
            images_directory.set_grouping_strategy(actions[users_choice])
            images_directory.add_grouping_factors_to_files()
            images_directory.copy_files()
            sys.exit()
        elif users_choice.lower() == "q":
            sys.exit("Goodbye!")
        else:
            print("Invalid input, try again.")
