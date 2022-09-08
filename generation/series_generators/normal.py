from decimal import Decimal
from numpy import log as ln
from numpy import sqrt
from numpy import pi
from numpy import cos
from numpy import exp as euler

from generation.series_generators.base import BaseSeriesGenerator


class NormalNumberGenerator(BaseSeriesGenerator):
    def __init__(self,
                 decimal_places,
                 random_number_generator,
                 mean=None,
                 variance=None,
                 standard_deviation=None):
        self.decimal_places = decimal_places
        self.random_number_generator = random_number_generator
        self.mean = float(mean)
        assert variance is not None or standard_deviation is not None, 'it should have at least one defined'
        if variance is not None:
            self.standard_deviation = sqrt(float(variance))
        else:
            self.standard_deviation = float(standard_deviation) 


    def generate_number(self):
        sum_random_numbers = 0
        for i in range(12):
            random_number = self.random_number_generator.generate_number()
            sum_random_numbers += random_number 
        #Metodo convolucion con k=12
        # [sumatoria(RND) -6]*desviacion estandar + media
        return self.truncate((sum_random_numbers - 6) * self.standard_deviation + self.mean, self.decimal_places)
    
    def get_expected_frequency(self, interval, sample_size, **kwargs):
        interval_size = (interval[1] - interval[0])
        class_mark = (interval[0] + interval[1])/2
        return int((1/(self.standard_deviation*sqrt(2*pi))*euler((-0.5)*((class_mark-self.mean)/self.standard_deviation)**2))*interval_size*sample_size)