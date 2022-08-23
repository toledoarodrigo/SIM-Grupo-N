import random
from generation.number_generator.base import BaseNumberGenerator

class LanguajeRandomGenerator(BaseNumberGenerator):
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
    
    def generate_number(self):
        return random.random()
