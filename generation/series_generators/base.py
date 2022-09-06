import math
from decimal import Decimal

from abc import ABC, abstractmethod

class BaseSeriesGenerator(ABC):
    number_generator = None
    default_lower_limit = None
    
    @staticmethod
    def truncate(number, digits) -> float:
        stepper = 10.0 ** digits
        return math.trunc(stepper * number) / stepper


    @abstractmethod
    def __init__(self,
                 decimal_places,
                 *args,
                 **kwargs):
        pass

    @abstractmethod
    def generate_number(self):
        pass