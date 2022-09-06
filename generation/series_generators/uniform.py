from decimal import Decimal
from generation.series_generators.base import BaseSeriesGenerator

class UniformNumberGenerator(BaseSeriesGenerator):
    def __init__(self,
                 decimal_places,
                 random_number_generator,
                 lower_limit=0,
                 upper_limit=0):
        self.lower_limit = float(lower_limit)
        self.upper_limit = float(upper_limit)
        self.random_number_generator = random_number_generator
        self.decimal_places = decimal_places

    def generate_number(self):
        random_number = self.random_number_generator.generate_number()
        # a + RND(b - a)
        return self.truncate(self.lower_limit + random_number * (self.upper_limit - self.lower_limit), self.decimal_places)
    
    def get_expected_frequency(self, interval, sample_size, **kwargs):
        intervals_amount = kwargs['intervals_amount']
        return sample_size / intervals_amount
