from abc import ABC
from abc import abstractmethod


class BaseNumberGenerator(ABC):
    @abstractmethod
    def generate_number(self, *args, **kwargs):
        pass

    