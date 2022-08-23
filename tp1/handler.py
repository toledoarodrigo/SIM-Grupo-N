# initial state indexes = [
#     numero de simulacion,
#     constante multiplicadora (a),
#     constante independiente (c),
#     modulo (m),
#     semilla (xn, o x0),
#     semilla 2 (xn-1 o x0),
#     generated_number,
#     random,
#     [last generated numbers, 20],
#     [frequency per interval]
# ]
initial_state_vector = [0, 0, 0, 0, 0, [], [0,0,0,0,0,0,0,0,0,0]]

def initialize_state(a, c, m, seed, seed_2=None):
    return [
        0,
        a,
        c,
        m,
        seed_2,
        None,
        seed,
        None,
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]
    ]

def get_frequency_index(value):
    for i in range(10):
        if ((i+1)*0.10 > value) or (i == 9 and (i+1)*0.10 >= value):
            return i
    return None

def build_state(prev_state, generated_number, random):
    iteration_number = prev_state[0] + 1
    seed = prev_state[6]
    seed_2 = prev_state[4]
    last_sim_number = prev_state[0]
    frequencies_acum = [*prev_state[8]]
    frequencies = [*prev_state[9]]
    freq_index = get_frequency_index(random)
    frequencies_acum[freq_index] = frequencies_acum[freq_index] + 1
    for i in range(10):
        extra = 0
        if i == freq_index:
            extra = 1
        frequencies[i] = (frequencies[i]*(last_sim_number) + extra) / iteration_number

    return [
        iteration_number,
        prev_state[1],
        prev_state[2],
        prev_state[3],
        seed,
        seed_2,
        generated_number,
        random,
        frequencies_acum,
        frequencies
    ]

def build_state_vector(state_vector, generated_number, random):
    prev_state = state_vector[len(state_vector) - 1]
    if len(state_vector)  == 2:
        state_vector.pop(0)
    new_state = build_state(prev_state, generated_number, random)
    return [prev_state, new_state]  

def generate_numbers(number_generator, iterations=20, state_vector=[], history_amount=20):
    history = []
    for i in range(iterations):
        state = state_vector[len(state_vector) - 1]
        seed, seed_2 = state[6], state[4]
        generated_number = number_generator.generate_number(seed, seed_2)
        random = number_generator.get_zero_padded_number(generated_number)
        state_vector = build_state_vector(state_vector, generated_number, random)
        if len(history) < history_amount:
            history.append(state_vector[len(state_vector) - 1])
    
    if (len(history) < state_vector[len(state_vector) - 1][0]):
        history.append(state_vector[len(state_vector) - 1])
    return history
