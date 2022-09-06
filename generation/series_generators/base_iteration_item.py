from abc import ABC
from abc import abstractmethod

class BaseIterationItem(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass