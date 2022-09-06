from abc import ABC, abstractmethod


class NumberGeneratorHandler(ABC):
    
    @staticmethod
    def instantiate_distribution_generator(generator_class, *args, **kwargs):
        return generator_class(*args, **kwargs)

    def __init__(self,
                 distribution_generator,
                 history_selector,
                 sample_size,
                 iteration_item_class,
                 *args, **kwargs):
        self.number_generator = distribution_generator
        self.history = []
        self.state_vector = []
        # Expects a function to add elemnts to the history
        self.history_selector = history_selector
        self.sample_size = int(sample_size)
        self.iteration_item_class = iteration_item_class
        self.iteration_item_kwargs = kwargs.get('iteration_item_kwargs', {})
        self.history_kwargs = kwargs.get('history_kwargs', {})

    def run(self):
        prev_element = None
        for i in range(self.sample_size):
            if len(self.state_vector) > 0:
                prev_element = self.state_vector[0]
            iteration_number = i + 1
            generated_number = self.number_generator.generate_number()
            self.iteration_item_kwargs["random_number"] = self.number_generator.random_number
            parsed_iteration = self.build_iterartion_data(iteration_number, generated_number, prev_element, **self.iteration_item_kwargs)
            if len(self.state_vector) > 1:
                self.state_vector.pop()
            self.state_vector.insert(0, parsed_iteration)
            history_item = self.history_selector(parsed_iteration, **self.history_kwargs)
            if history_item is not None:
                self.history.append(history_item)

    def build_iterartion_data(self, *args, **kwargs):
        iteration_item = self.iteration_item_class(*args, **kwargs)
        return iteration_item.__dict__
