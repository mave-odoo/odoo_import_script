# -*- coding: utf-8 -*-

import sys
import csv
import os
import json
import unidecode
import re


substr_img = 'http://drive.google.com'

with open('images_path.json') as json_file:
    images_data = json.load(json_file)


def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            jsonArray.append(row)

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)


def dict_to_json(dictionnary, jsonFilePath):
    json_object = json.dumps(dictionnary, indent=4)
    with open(jsonFilePath, "w") as f:
        f.write(json_object)


def create_matrix(rows):
    matrix = []
    for row in rows:
        matrix.append(row)
    return matrix


def fill_failed_row(headers, row):
    dictionnary = {
        "data": {}
    }
    for i, head in enumerate(headers):
        dictionnary["data"][head] = row[i]
    dictionnary["FAILED REASON"] = "Img Not found"
    return dictionnary


def delete_logs_files(file_name):
    if os.path.exists(f"./logs/fails/FAILS_{file_name}.json"):
        os.remove(f"./logs/fails/FAILS_{file_name}.json")
    if os.path.exists(f"./results/csv/RESULT_{file_name}.csv"):
        os.remove(f"./results/csv/RESULT_{file_name}.csv")
    if os.path.exists(f"./results/json/RESULT_{file_name}.json"):
        os.remove(f"./results/json/RESULT_{file_name}.json")


def get_item_id(id):
    regex = re.compile(r"[A-Z0-9].*$")
    matches = regex.findall(id)
    if len(matches) == 0:
        return ""
    return matches[0]


def get_image_col_index(headers):
    regex = re.compile(r'.*[iI]mage')
    for head in headers:
        if regex.match(head):
            return headers.index(head)
    return -1


def parse_csv(csv_path):

    stats_str = ""

    csv_file_name = csv_path.replace(sys.argv[1], "").replace(".csv", "")

    if csv_file_name[0] == '/':
        csv_file_name = csv_file_name[1:]

    stats_str += f"{csv_path}\n"

    matches_found = 0
    failed = {}

    with open(csv_path, 'r') as f:
        csvreader = csv.reader(f)

        headers = next(csvreader)

        img_col_index = get_image_col_index(headers)

        matrix = create_matrix(csvreader)

        lines_nbr = len(matrix)
        stats_str += f"LINES NBR: {lines_nbr}\n"

        for y, row in enumerate(matrix):
            if img_col_index == -1:
                break

            found = False

            for x, item in enumerate(row):
                item_value = ''.join(filter(str.isalnum, unidecode.unidecode(get_item_id(row[x]))))
                if item_value in images_data:
                    matrix[y][img_col_index] = images_data[item_value]
                    matches_found += 1
                    found = True
                    break

            # If no match found
            if not found:
                failed[f"Line {y}"] = fill_failed_row(headers, row)
                matrix[y][img_col_index] = ""

        print(f">> MATCHES FOUND: {matches_found} || FAILED: {lines_nbr - matches_found}")
        stats_str += f"MATCHES FOUND: {matches_found} || FAILED: {lines_nbr - matches_found}\n\n"

        dict_to_json(failed, f"./results/logs/fails/FAILS_{csv_file_name}.json")

    csv_result_name = f"./results/csv/RESULT_{csv_file_name}.csv"
    json_result_name = f"./results/json/RESULT_{csv_file_name}.json"

    print(f"> \"./results/csv/RESULT_{csv_file_name}.csv\" CREATED\n")


    with open(csv_result_name, 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(headers)
        writer.writerows(matrix)

    csv_to_json(csv_result_name, json_result_name)

    with open("./results/logs/stats.txt", 'a') as f:
        f.write(stats_str)


def check_files():
    if os.path.exists("./results/logs/stats.txt"):
        os.remove("./results/logs/stats.txt")

    if not os.path.exists("./results/"):
        os.makedirs("./results/")

    if not os.path.exists("./results/csv"):
        os.makedirs("./results/csv")

    if not os.path.exists("./results/json"):
        os.makedirs("./results/json")

    if not os.path.exists("./results/logs"):
        os.makedirs("./results/logs")

    if not os.path.exists("./results/logs/fails"):
        os.makedirs("./results/logs/fails")


if __name__ == "__main__":
    print("##############################")
    print("####### CSV REPLACING ########")
    print("##############################\n")

    check_files()

    for csv_file in os.listdir(sys.argv[1]):
        f = os.path.join(sys.argv[1], csv_file)
        if os.path.isfile(f):
            print(f">>> Browsing \"{f}\"")
            file_name = f.replace(sys.argv[1], "").replace(".csv", "")
            delete_logs_files(file_name)
            parse_csv(f)
