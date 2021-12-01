# imagine - picture sorting script
## General info
Script to sort pictures dumped from mobile phone or digital camera.
## Requirements
- Pillow library 8.4.0
## How to use
```
$ cd ~/download_directory/imagine
$ pip install -r requirements.txt
$ python3 imagine.py <here enter directory of images you want to sort>
```
## Features
During each run script creates a directory that contains sub-directories with images sorted by different criteria. Currently it is possible to sort according to:  
- year or month - images are sorted into folders representing different years or months
- year and month - two-level sorting, first by years, then by months
- place - if images have GPS coordinates in their EXIF data, they are grouped together if the distance between them is not exceeding declared value (currently hard coded to 200 meters)
- Smart Grouping - Images are grouped by places (see above), but also they are assigned a time span. Thanks to that, if user have been to the same place in the summer and then in the winter, the photos will end up in two different folders, which name will contain the place's id and also the time span in which the photos were taken.
