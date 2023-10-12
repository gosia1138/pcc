# imagine - picture sorting script
## General info
Script to sort pictures dumped from mobile phone or digital camera.
## Requirements
- Python 3.10
- Pillow
- pytest
- pipenv
## How to use
```
$ cd ~/download_directory/imagine
$ python -m pip install pipenv
$ pipenv install
$ pipenv shell
$ python main.py <here enter directory of images you want to sort> <grouping factor>
```

Grouping factors options:
```
  -y, --year   Group images in given directory by year
  -m, --month  Group images in given directory by month
  -d, --date   Group images in given directory by year and then month
  -p, --place  Group images in given directory by place
  -s, --smart  Smart Grouping (place and date)
``` 

So for example to group pictures from mixed_photos subfolder of your Pictures folder by places and dates (Smart Grouping) the command used should look as follows:
```

```
## Features
During each run script creates a directory that contains sub-directories with images sorted by different criteria. Currently it is possible to sort according to:  
- year or month - images are sorted into folders representing different years or months
- year and month - two-level sorting, first by years, then by months
- place - if images have GPS coordinates in their EXIF data, they are grouped together if the distance between them is not exceeding declared value.
- Smart Grouping - Images are grouped by places (see above), but also they are assigned a time span. Thanks to that, if user have been to the same place in the summer and then in the winter, the photos will end up in two different folders, which name will contain the place's id and also the time span in which the photos were taken.
