import pandas as pd
import os
from tkinter import messagebox
import chardet

NUMBER_OF_COLUMNS_OF_FILE = 218


def get_files():
    dir = os.getcwd()
    if files := [
        os.path.join(dir, file) for file in os.listdir(".") if file.endswith(".csv")
    ]:
        return files
    else:
        files = [
            os.path.join(dir, file)
            for file in os.listdir(".")
            if file.endswith(".xlsx") and file != "SII EMITIDAS CLIENTES.xlsx"
        ]
        return files


def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
    return result["encoding"]


def check_same_columns(files, encodi):
    first_file_columns = None
    for file in files:
        df = read_file(file, encodi, 1)
        if first_file_columns is None:
            first_file_columns = df.columns
        elif not df.columns[:NUMBER_OF_COLUMNS_OF_FILE].equals(
            first_file_columns[:NUMBER_OF_COLUMNS_OF_FILE]
        ):
            messagebox.showerror("ERROR", "Los archivos no tienen las mismas columnas.")
            exit()
    return True


def read_file(file, encodi, nrows=None):
    if file.endswith(".csv"):
        df = pd.read_csv(file, encoding=encodi, delimiter=";", nrows=nrows)
    else:
        df = pd.read_excel(file, nrows=nrows)
    return df
