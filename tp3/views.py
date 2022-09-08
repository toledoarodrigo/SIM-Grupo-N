from django.shortcuts import render

from generation.number_generator.languaje import LanguajeRandomGenerator
from generation.series_generators.poisson import PoissonNumberGenerator
from generation.series_generators.uniform import UniformNumberGenerator
from generation.series_generators.normal import NormalNumberGenerator
from generation.series_generators.exponential import ExponentialNumberGenerator

from tp1.pruebas import chi_cuadrado, obtener_chi_tabla, get_chi_test_result

from tp3.number_generator_handler import TP3NumberGeneratorHandler as NumberGeneratorHandler
from tp3.iteration_item import IterationItem


def index(request):
    return render(request, 'index.html', {})

UNIFORM = 'uniform'
NORMAL = 'normal'
EXPONENTIAL = 'exponential'
POISSON = 'poisson'

DISTRIBUTION_MAPPING = {
    UNIFORM: UniformNumberGenerator,
    NORMAL: NormalNumberGenerator,
    EXPONENTIAL: ExponentialNumberGenerator,
    POISSON: PoissonNumberGenerator
}

def select_item(iteration_item, *args, **kwargs):
    return iteration_item

def generate_series(request):
    data = request.POST
    is_discrete = data.get("distribution") == POISSON
    distribution_generator_class = DISTRIBUTION_MAPPING[data.get("distribution")]
    distribution_arguments = [int(data.get("decimal_places", 4)), LanguajeRandomGenerator(), *data.getlist(f"{data.get('distribution')}_args")]
    # Inicializaion del generador de numeros aleatorios segun lo elegido en el Front end.
    distribution_generator = NumberGeneratorHandler.instantiate_distribution_generator(distribution_generator_class, *distribution_arguments)
    number_generator = NumberGeneratorHandler(
        distribution_generator,
        select_item,
        data['sample_size'],
        IterationItem,
        intervals_amount=int(data['intervals_amount']),
        discrete=is_discrete
    )
    number_generator.run()
    import json

    # Inicia test de chi cuadrado
    observed_frequencies = []
    expected_frequencies = []
    intervals = []
    for interval, value in number_generator.frequencies.items():
        expected, observed = value
        observed_frequencies.append(observed)
        expected_frequencies.append(expected)
        intervals.append(interval)
    # Armado de tabla de chi cuadarado
    chi_cuad = chi_cuadrado(observed_frequencies, int(data['intervals_amount']), expected_frequencies, int(data.get("decimal_places", 4)), intervals_list=intervals)
    # Chi tabluado
    chi_en_tabla = obtener_chi_tabla(int(data['intervals_amount']))
    # Chi calculado
    last_chi = chi_cuad[-1][-1]
    # Obtengo el resultado del test de chi (Rechaza/No Rechaza)
    test_result = get_chi_test_result(chi_cuad, chi_en_tabla)

    return render(request, 'results.html', {
        'history': number_generator.history,
        'history_str': json.dumps(number_generator.history), 
        'labels': number_generator.frequencies.keys(),
        'values': number_generator.frequencies.values(),
        'frequencies': number_generator.frequencies,
        'isDiscrete': is_discrete,
        "chi_cuad": chi_cuad,
        "chi_en_tabla": chi_en_tabla,
        "calculated_chi": last_chi,
        "test_result": test_result,
    })