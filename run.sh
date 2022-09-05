#!/bin/bash

# $1 images directory path
# $2 .csv files directory path

rm -rf ./results

python3 ./scripts/parse_images.py $1
python3 ./scripts/parse_csv.py $2
python3 ./scripts/encode_images.py $2
python3 ./scripts/import_data.py $2

rm images_path.json

echo "DONE"