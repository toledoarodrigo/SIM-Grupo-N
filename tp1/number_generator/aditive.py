from generation.number_generator.base import BaseNumberGenerator
from generation.utils import truncate

class Aditive(BaseNumberGenerator):
    def __init__(self, m):
        self.m = m

    def generate_number(self, seed, seed_2, *args, **kwargs):
        return (seed + seed_2) % self.m
    
    def get_zero_padded_number(self, generated_number, decimal_places=4):
        return truncate(generated_number/ (self.m - 1), decimal_places)
