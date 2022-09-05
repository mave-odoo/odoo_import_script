# -*- coding: utf-8 -*-

import sys
import csv
import os
import json
import unidecode
from fnmatch import fnmatch

images_dir = os.scandir(sys.argv[1])
patterns = ['*.png', '*.PNG', '*.jpg', '*.JPG', '*.jpeg', '*.JPEG']

values = {}


if __name__ == "__main__":
    print("##############################")
    print("####### IMAGES PARSING #######")
    print("##############################\n")
    print(f"> Reading images in {sys.argv[1]}\n")

    # Browsing all directories/sub-directories and map every image_name to its path
    for pattern in patterns:
        for path, subdirs, files in os.walk(sys.argv[1]):
            for name in files:
                if fnmatch(name, pattern):
                    img_id = ''.join(filter(str.isalnum, os.path.splitext(unidecode.unidecode(name))[0]))
                    values[img_id] = os.path.join(path, name)

    # Serializing json
    json_object = json.dumps(values, indent=4)

    # Writing to images_path.json
    with open("images_path.json", "w") as outfile:
        outfile.write(json_object)