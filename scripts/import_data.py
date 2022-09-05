# -*- coding: utf-8 -*-

import os
import csv
import subprocess
import ctypes as ct


model_names = [
    "product_category",
    "product_public_category",
    "product_attribute",
    "product_template",
    "product_product"
]


def get_model(csv_path):
    with open(csv_path, "r") as f:
        csvreader = csv.reader(f)

        # Removing headers line
        next(csvreader)

        first_row = next(csvreader)

        for model_name in model_names:
            if model_name in first_row[0]:
                return model_name.replace("_", ".")

        return "MODEL NOT FOUND"


def import_data(csv_path):
    model = get_model(csv_path)

    tokens = [
        "odoo_import_thread.py",
        "-c",
        "./connection.conf",
        f"--file={csv_path}",
        f"--model={model}",
        "--worker=2",
        "--size=1",
        "--sep=,"
    ]

    result = subprocess.run(tokens, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    print(result.stderr)


if __name__ == "__main__":
    print("##############################")
    print("######### IMPORT DATA ########")
    print("##############################\n")

    csv.field_size_limit(int(ct.c_ulong(-1).value // 2))

    for csv_file in sorted(os.listdir("./results/csv")):
        print(f"> Importing data from \"{csv_file}\"")
        f = os.path.join("./results/csv", csv_file)
        if os.path.isfile(f):
            import_data(f)
