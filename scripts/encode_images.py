# -*- coding: utf-8 -*-

import sys
import csv
import os
import re
import base64


def create_matrix(rows):
    matrix = []
    for row in rows:
        matrix.append(row)
    return matrix


def get_image_col_index(headers):
    regex = re.compile(r'.*[iI]mage')
    for head in headers:
        if regex.match(head):
            return headers.index(head)
    return -1


def encode_images(csv_path):
    with open(csv_path, "r") as f:
        csvreader = csv.reader(f)

        headers = next(csvreader)

        img_col_index = get_image_col_index(headers)

        matrix = create_matrix(csvreader)
        if img_col_index != -1:
            for y, row in enumerate(matrix):
                if row[img_col_index] == '':
                    continue
                with open(row[img_col_index], "rb") as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode()
                    row[img_col_index] = img_base64

    with open(csv_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(matrix)


if __name__ == "__main__":
    print("##############################")
    print("####### IMAGES ENCODING ######")
    print("##############################\n")

    for csv_file in os.listdir("./results/csv"):
        f = os.path.join("./results/csv", csv_file)
        print(f"> Encoding images in {f}\n")
        if os.path.isfile(f):
            encode_images(f)
