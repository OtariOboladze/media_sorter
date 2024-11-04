'''
Put this script in a messy folder filled with images and video files 
and run it to create a "Years" folder with the media files sorted by months in each year.

You can also change what types of files to look for in your folder
by simply adding to or changing the following lists: `imgFormats` and `videoFormats`.

NOTE: This script can also delete duplicates (by searching for " 2" at the end of file names) and files starting with "._".
This is disabled by default, to enable set `DELETE` flag to True!
'''

import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

DATE_TIME_ORIG_TAG = 36867
DELETE = False

# create a list of image and video formats
imgFormats = ['png', 'jpg', 'jpeg']
videoFormats = ['m4v', 'mov', 'mp4']

# iterate over all files in the current directory and subdirectories
for root, dirs, files in os.walk('.'):
    for afile in files:
        filename = os.fsdecode(afile)
        filepath = os.path.join(root, filename)
        print("Processing %s\n" % filepath)
        name = filename.split('.')[0]

        # skip directories
        if os.path.isdir(filepath):
            continue

        # check if the file name ends with " 2" and delete it
        elif name[-2:] == ' 2' and DELETE:
            print("Renaming %s\n" % name)
            ext = filename.split('.')[1]
            try:
                os.rename(filepath, os.path.join(root, name[:-1].strip() + '.' + ext))
            except FileExistsError:
                print("Found existing file %s - Deleting\n" % name)
                os.remove(os.path.join(root, name[:-1].strip() + '.' + ext))
                os.rename(filepath, os.path.join(root, name[:-1].strip() + '.' + ext))
            continue

        # check if the file is a python file
        elif filename.endswith(".py"):
            continue

        # check if the file starts with "._" and delete it
        elif filename.startswith("._") and DELETE:
            print("Deleting %s\n" % filepath)
            os.remove(filepath)
            continue

        # check if the file is an image and has EXIF data
        elif filename.split('.')[1].lower() in imgFormats:
            try:
                im = Image.open(filepath)
                exif = im._getexif()
                im.close()
                if DATE_TIME_ORIG_TAG in exif:
                    print("Has EXIF: %s\n" % exif[DATE_TIME_ORIG_TAG])
                    datestr = exif[DATE_TIME_ORIG_TAG].split()
                    dateobj = datetime.strptime(datestr[0], "%Y:%m:%d")
                    dirpath = os.path.join("Years", str(dateobj.year), str(dateobj.month))
                    os.makedirs(dirpath, exist_ok=True)
                    os.rename(filepath, os.path.join(dirpath, filename))
                continue
            except:
                continue

        # check if the file is a video and has metadata
        elif filename.split('.')[1].lower() in videoFormats:
            parser = createParser(filepath)
            if not parser:
                print("Unable to parse file %s" % filepath)
                continue
            with parser:
                try:
                    metadata = extractMetadata(parser)
                except Exception as err:
                    print("Metadata extraction error: %s" % err)
                    metadata = None
            if not metadata:
                print("Unable to extract metadata")
                continue
            for line in metadata.exportPlaintext():
                if line.split(':')[0] == '- Creation date':
                    dateobj = datetime.strptime(
                        line.split(':')[1].split()[0], "%Y-%m-%d")
                    dirpath = os.path.join("Years", str(dateobj.year), str(dateobj.month))
                    os.makedirs(dirpath, exist_ok=True)
                    os.rename(filepath, os.path.join(dirpath, filename))