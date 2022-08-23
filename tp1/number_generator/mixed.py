from generation.number_generator.base import BaseNumberGenerator
from generation.utils import truncate

class Mixed(BaseNumberGenerator):
    def __init__(self, a, m, c):
        self.a = a
        self.m = m
        self.c = c

    def generate_number(self, seed, *args, **kwargs):
        return (self.c + self.a * seed) % self.m
    
    def get_zero_padded_number(self, generated_number, decimal_places=4):
        return truncate(generated_number/ (self.m - 1), decimal_places)
