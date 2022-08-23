from generation.number_generator.base import BaseNumberGenerator
from generation.utils import truncate

class Multiplicative(BaseNumberGenerator):
    def __init__(self, a, m, x0):
        self.x = x0
        self.a = a
        self.m = m
        self.c = 0

    def generate_number(self):
        return self.x

    def generate_number(self, seed, *args, **kwargs):
        return (self.c + self.a * seed) % self.m
    
    def get_zero_padded_number(self, generated_number, decimal_places=4):
        return truncate(generated_number/ (self.m - 1), decimal_places)
