import pandas as pd
import re


def function_as_parameter(row):
    # Suma para cada fila todas las bases que tienen el tipo que se le pasa como argumento
    bases_tipoDeseado_fila = []
    for index, column in enumerate(row.index):
        if re.search(r".*Causa Exenta.*", column):
            previous_value = row[row.index[index - 1]]
            if pd.isna(previous_value):
                continue
            if pd.isna(row[column]):
                bases_tipoDeseado_fila.append(previous_value)
    return sum(bases_tipoDeseado_fila)


def func_calculate_bases_cosa_rara(df):
    df["Otros"] = df.apply(function_as_parameter, axis=1)
    return df
