from decimal import Decimal
from numpy import log as ln
from numpy import sqrt
from numpy import exp as euler

from generation.series_generators.base import BaseSeriesGenerator


class ExponentialNumberGenerator(BaseSeriesGenerator):
    default_lower_limit = 0

    def __init__(self,
                 decimal_places,
                 random_number_generator,
                 mean=0):
        self.decimal_places = decimal_places
        self.random_number_generator = random_number_generator
        self.mean = float(mean)
        self.lower_limit = self.default_lower_limit

    def generate_number(self):
        random_number = self.random_number_generator.generate_number()
        # (-1/lambda)*ln(1-RND) with lambda = 1/mean
        return self.truncate((-1 / (1 / self.mean))*ln(1 - random_number), self.decimal_places)

    def get_expected_frequency(self, interval, sample_size, **kwargs):
        interval_size = (interval[1] - interval[0])
        class_mark = (interval[0] + interval[1])/2
        lambda_value = 1 / self.mean
        return int(lambda_value * euler(-lambda_value*class_mark)*interval_size*sample_size)