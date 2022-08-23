from django.shortcuts import render
from tp1.number_generator.mixed import Mixed
from tp1.number_generator.multiplicative import Multiplicative
from tp1.number_generator.aditive import Aditive
from tp1.handler import generate_numbers, initialize_state
from tp1.utils import histogram
from tp1.utils import frecuencias_esperadas
from tp1.pruebas import chi_cuadrado, obtener_chi_tabla, get_chi_test_result

# Create your views here.
def index(request):
    return render(request, 'tp1/index.html', {})

def generate(request):
    data = request.POST
    c = None
    a = data["a"]
    m = data["m"]
    generator = data["generator"]
    seed = data["seed"]
    seed_2 = None
    iterations = int(data.get("iterations", 20))
    history_amount = data.get("history_amount", 20)
    intervals = 10
    total_iterations = int(data.get('n', None))
    if (iterations > total_iterations):
        iterations = total_iterations
    if (data['generator'] == "mixed"):
        c = int(data["c"])
        a = int(a)
        number_generator = Mixed(
            a,
            int(m),
            c,
        )
        generator_display = "Mixto"
    if (data['generator'] == "multiplicative"):
        a = int(a)
        number_generator = Multiplicative(
            a,
            int(m),
        )
        c = None
        generator_display = "Multiplicativo"
    if (data["generator"] == "aditive"):
        generator_display = "Aditivo"
        number_generator = Aditive(
            int(m),
        )
        a = None
        seed_2 = int(data["seed_2"])
    state_vector = [
        initialize_state(
            a,
            c,
            int(m),
            int(seed),
            seed_2=seed_2
        )
    ]
    history = generate_numbers(number_generator, iterations=int(iterations), state_vector=state_vector, history_amount=int(history_amount))
    acums = history[len(history)-1][8]
    histogram64 = histogram(acums, 10)
    chi_cuad = chi_cuadrado(acums, intervals)
    chi_en_tabla = obtener_chi_tabla(intervals)
    last_chi = chi_cuad[-1][-1]
    test_result = get_chi_test_result(chi_cuad, chi_en_tabla)
    return render(request, 'tp1/generation_results.html', {
        "history":history,
        "generator_display": generator_display,
        "generator": generator,
        "seed": seed,
        "seed_2": seed_2,
        "a":a,
        "c":c,
        "m":m,
        "history_amount": history_amount,
        "iterations": iterations,
        "total_iterations": total_iterations,
        "histogram": histogram64,
        "chi_cuad": chi_cuad,
        "chi_en_tabla": chi_en_tabla,
        "calculated_chi": last_chi,
        "test_result": test_result,
    })
