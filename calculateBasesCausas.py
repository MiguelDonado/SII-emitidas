import pandas as pd
import re


def function_as_parameter(row, causa):
    # Suma para cada fila todas las bases que tienen la causa que se le pasa como argumento
    bases_causaDeseado_fila = []
    for index, column in enumerate(row.index):
        if re.search(r".*Causa Exenta.*", column):
            previous_value = row[row.index[index - 1]]
            if row[column] == causa:
                bases_causaDeseado_fila.append(previous_value)
    return sum(bases_causaDeseado_fila)


def func_calculate_bases_causas(df):
    # E2 = Exportaciones; E5 = Entregas intracomunitarias
    # causas = Causas Exención
    causas = ["E2", "E5"]
    for causa in causas:
        if causa == "E2":
            name_column = "Exportaciones"
        elif causa == "E5":
            name_column = "Entregas intracomunitarias"
        # Apply to each row of the dataframe the next function, and return
        df[name_column] = df.apply(function_as_parameter, args=(causa,), axis=1)
    return df
