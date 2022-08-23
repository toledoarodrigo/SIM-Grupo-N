import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import urllib, base64

def frecuencias_esperadas(total_numbers, intervals):
    esperados = []
    rango_intervalos = 1 / intervals
    frecuencia_esperada = total_numbers // intervals
    resto = total_numbers % intervals
    valores = rango_intervalos / 2
    for i in range(intervals):
        esperados.append(frecuencia_esperada)
    # for i in range(intervals):
    #     for j in range(frecuencia_esperada):
    #         esperados.append(valores)
    #     valores += rango_intervalos
    # if resto:
    #     valores = rango_intervalos / 2
    #     for j in range(resto):
    #         esperados.append(valores)
    #         valores += rango_intervalos
    return esperados

def histogram(numbers, intervals):
    histogram = create_comparative_histogram(numbers, intervals)
    flike = io.BytesIO()
    histogram.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    return b64
    
def create_histogram(acums, intervals):
    total_numbers = 0
    for acum in acums:
        total_numbers += acum
    plt.close() #En caso de nueva consulta, se borra el plt anterior
    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    esperados = frecuencias_esperadas(total_numbers, intervals)
    data = np.column_stack((acums, esperados))
    combinado = [acums, esperados]
    n, bins, patches = plt.hist(data, bins=intervals, alpha=.5, range=(0,1), label=['F Obs','F Esp'])
    ax.tick_params(axis='both', labelsize=8)
    plt.title('Histograma de resultados')
    plt.xlabel('Intervalos')
    plt.ylabel('Frecuencia')
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
    plt.grid(linestyle="--", linewidth=0.5, color='.25')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xticks(bins)
    return plt

def create_comparative_histogram(acums, intervals):
    total_numbers = 0
    for acum in acums:
        total_numbers += acum
    plt.close() #En caso de nueva consulta, se borra el plt anterior
    fig, ax = plt.subplots()
    esperados = frecuencias_esperadas(total_numbers, intervals)
    x = np.arange(intervals)
    width = 0.5
    rectsObserved = ax.bar(x - 0.75, acums, width, label='F Obs')
    rectsExpected = ax.bar(x - 0.25, esperados, width, label='F Esp')

    # ax.tick_params(axis='both', labelsize=8)
    plt.title('Histograma de resultados')
    plt.xlabel('Intervalos')
    plt.ylabel('Frecuencia')
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
    ax.set_xticks( x, [("0-0.1"), ("0.1-0.2"), ("0.2-0.3"), ("0.3-0.4"), ("0.4-0.5"), ("0.5-0.6"), ("0.6-0.7"), ("0.7-0.8"), ("0.8-0.9"), ("0.9-1.0")])

    ax.bar_label(rectsObserved, padding=3)
    ax.bar_label(rectsExpected, padding=3)
    fig.tight_layout()
    return plt