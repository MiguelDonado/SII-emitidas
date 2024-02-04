import pandas as pd
from introFunc import get_files_csv, get_files_xlsx, check_same_columns, detect_encoding
from supportFuncPand import calculate_all_columns, delete_columns

from calculateBasesCausas import func_calculate_bases_causas
from calculateBasesTipos import func_calculate_bases_tipos
from calculateCosaRara import func_calculate_bases_cosa_rara

from output import write_to_xlsx


def main():
    files_csv = get_files_csv()
    if not files_csv:
        files_xlsx = get_files_xlsx()
        files = files_xlsx
    else:
        files = files_csv
    encodi = detect_encoding(files[0])
    if check_same_columns(files, encodi):
        df = merge_files(files, encodi)
        df = calculate_all_columns(df)
        df = func_calculate_bases_causas(df)
        df = func_calculate_bases_tipos(df)
        df = func_calculate_bases_cosa_rara(df)
        df = delete_columns(df)
        write_to_xlsx(df)


def merge_files(files, encodi):
    # Merge files and drop empty rows and columns, and filter only the desired columns
    # load all files into a list of dataframes
    if files[0].endswith(".csv"):
        dfs = [pd.read_csv(file, encoding=encodi, delimiter=";") for file in files]
    else:
        dfs = [pd.read_excel(file) for file in files]
    # concatenate dataframes
    merged_df = pd.concat(dfs, ignore_index=True)
    # drop rows where Nombre o Razón Social Factura Emisor is empty (these are the rows that contain the totals)
    merged_df.dropna(subset=["Nombre o Razón Social Destinatario"], inplace=True)
    # drop columns that are completely empty
    merged_df.dropna(how="all", axis=1, inplace=True)
    # filter Dataframe to include the desired columns
    merged_df = merged_df.filter(
        regex=".*Serie.*Factura|Fecha Expedición|Descripción Operación|NIF Destinatario|Nombre o Razón Social Destinatario|\(.*Base Imponible.*|.*Causa Exenta.*|.*Tipo Impositivo.*|.*Repercutida.*|Estado Cuadre",
    )
    return merged_df


main()
