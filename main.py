import sys
from pcc.directory import Directory, JPGFilterStrategy
from pcc.utils.grouping_strategies import (
    YearGroupingStrategy,
    MonthGroupingStrategy,
    YearMonthGroupingStrategy,
    PlaceGroupingStrategy,
    TimePlaceGroupingStrategy)
import argparse
from pathlib import Path


grouping_actions_strategies = {
        1: YearGroupingStrategy,
        2: MonthGroupingStrategy,
        3: YearMonthGroupingStrategy,
        4: PlaceGroupingStrategy,
        5: TimePlaceGroupingStrategy
    }


if __name__ == '__main__':
    grouping_strategies = []
    parser = argparse.ArgumentParser(
        prog="PCC - Photo Chaos Controller",
        usage='main.py <directory> <grouping factors>',
        description='''Program to sort photos by chosen factors. You can choose one or more grouping factors,
        they will be applied in the same order as you put them in the prompt.'''
        )
    parser.add_argument("directory", help="Directory to images you want to group", type=Path)
    grouping_factor = parser.add_argument_group()
    grouping_factor.add_argument("-y", "--year", help="Group images in given directory by year", dest='grouping_factors', action='append_const', const=1)
    grouping_factor.add_argument("-m", "--month", help="Group images in given directory by month", dest='grouping_factors', action='append_const', const=2)
    grouping_factor.add_argument("-d", "--date", help="Group images in given directory by year and then month", dest='grouping_factors', action='append_const', const=3)
    grouping_factor.add_argument("-p", "--place", help="Group images in given directory by place", dest='grouping_factors', action='append_const', const=4)
    grouping_factor.add_argument("-s", "--smart", help="Smart Grouping (place and date)", dest='grouping_factors', action='append_const', const=5)
    
    args = parser.parse_args()
    args_grouping_factors = args.grouping_factors
    args_directory = args.directory
    if not args_grouping_factors or not args_directory:
        parser.error('No any grouping factors provided - please provide at least one')

    directory = Directory(args_directory, JPGFilterStrategy)
    grouping_strategies = list(map(lambda x: grouping_actions_strategies.get(x), args_grouping_factors))

    for grouping_strategy in grouping_strategies:
        directory.set_grouping_strategy(grouping_strategy)
        directory.add_grouping_factors_to_files()
    directory.copy_files()

    print(f"\n{directory.get_number_of_files()} images from {directory.directory} processed successfully!")