import pandas as pd
import os
from tkinter import messagebox
import chardet


def get_files_csv():
    # Get all csv files from actual directory
    dir = os.getcwd()
    files = [
        os.path.join(dir, file) for file in os.listdir(".") if file.endswith(".csv")
    ]
    return files


def get_files_xlsx():
    # Get all xlsx files from actual directory
    dir = os.getcwd()
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
    if files[0].endswith(".csv"):
        # Check if all the csv files've the same columns.
        first_file_columns = None
        for file in files:
            # read only the first row
            df = pd.read_csv(file, encoding=encodi, delimiter=";", nrows=1)
            if first_file_columns is None:
                first_file_columns = df.columns
            elif not df.columns[:218].equals(first_file_columns[:218]):
                messagebox.showerror(
                    "ERROR",
                    "Los archivos no tienen las mismas columnas.",
                )
                exit()
    else:
        # Check if all the xlsx files've the same columns.
        first_file_columns = None
        for file in files:
            # read only the first row
            df = pd.read_excel(file, nrows=1)
            if first_file_columns is None:
                first_file_columns = df.columns
            elif not df.columns[:218].equals(first_file_columns[:218]):
                messagebox.showerror(
                    "ERROR", "Los archivos no tienen las mismas columnas."
                )
                exit()
    return True
