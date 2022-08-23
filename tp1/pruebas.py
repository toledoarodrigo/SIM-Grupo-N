import numpy as np
from generation.utils import truncate

tableChiCu= [3.84, 5.99, 7.81, 9.49, 11.1, 12.6, 14.1, 15.5, 16.9, 18.3, 
            19.7, 21.0, 22.4, 23.7, 25.0, 26.3, 27.6, 28.9, 30.1, 31.4, 
            32.7, 33.9, 35.2, 36.4, 37.7, 38.9, 40.1, 41.3, 42.6, 43.8]

def chi_cuadrado(cumulatives, intervals):
    table = []
    length = 0
    for interval_cumulative in cumulatives:
        length += interval_cumulative
    hist = np.histogram(cumulatives, bins=intervals, range=(0,1))
    esperada = length // intervals
    chi_acumulado = 0
    for i in range(intervals):
        intervalo_label = str(round(hist[1][i], 2)) + ' - ' + str(round(hist[1][i+1], 2))
        frecuencia_obs = cumulatives[i]
        resto = length % intervals
        if  (resto > 0 and resto > i):
            frecuencia_esp = esperada + 1
        else:
            frecuencia_esp = esperada
        chi_linea = truncate(((frecuencia_esp - frecuencia_obs)**2) / frecuencia_esp, 4)
        chi_acumulado += chi_linea
        chi_acumulado = truncate(chi_acumulado, 4)
        table_line = [intervalo_label, frecuencia_obs, frecuencia_esp, chi_linea, chi_acumulado]
        table.append(table_line)
    return table

def obtener_chi_tabla(intervals):
    gradoLibertad=intervals-1
    chiCuaTab=tableChiCu[(gradoLibertad-1)]
    return chiCuaTab 

def get_chi_test_result(chi_table, spected_chi):
    last_chi = chi_table[-1][-1]
    positive_str = "No se puede rechazar la hipotesis nula"
    negative_str = "Se rechaza la hipotesis nula"
    return positive_str if last_chi <= spected_chi else negative_str
