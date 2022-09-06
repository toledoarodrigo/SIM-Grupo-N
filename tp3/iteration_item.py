from generation.series_generators.base_iteration_item import BaseIterationItem


class IterationItem(BaseIterationItem):
    def __init__(self, iteration, generated_number, prev_element, **kwargs):
        self.iteration = iteration
        generated_number = generated_number
        self.generated_number=generated_number
        self.maximum = self.generated_number
        self.minimum = self.generated_number
        if prev_element is not None:
            self.maximum = generated_number if generated_number > prev_element['maximum'] else prev_element['maximum']
            self.minimum = generated_number if generated_number < prev_element['minimum'] else prev_element['minimum']
