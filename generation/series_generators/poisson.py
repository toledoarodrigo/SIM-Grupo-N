from decimal import Decimal
import math
from generation.series_generators.base import BaseSeriesGenerator

class PoissonNumberGenerator(BaseSeriesGenerator):
    def __init__(self,
                 decimal_places,
                 random_number_generator,
                 mean=0):
        self.random_number_generator = random_number_generator
        self.decimal_places = decimal_places
        self.mean = float(mean)

    def generate_number(self):
        x = 0
        h = math.e ** self.mean
        while True:
            u = self.random_number_generator.generate_number()
            h = h * u
            if h < 1:
                break
            x += 1
        return x
    
    def get_expected_frequency(self, interval, sample_size, **kwargs):
        class_mark = int(interval[0])
        return int((((self.mean ** class_mark)/math.factorial(class_mark))*(math.e **(-self.mean)))*sample_size)
