from generation.series_generators.generator_handler import NumberGeneratorHandler


class TP3NumberGeneratorHandler(NumberGeneratorHandler):
    def build_observed_frequencies(self):
        observed_frequencies = {}
        if self.intervals is None:
            last_item = self.history[len(self.history) - 1]
            self.intervals = self.generate_intervals(self.number_generator, self.intervals_amount, last_item['minimum'], last_item['maximum'], self.isDiscrete)
        for frequency in self.intervals:
            observed_frequencies[frequency] = (
                self.number_generator.get_expected_frequency(frequency, self.sample_size,
                intervals_amount=self.intervals_amount), 0)
        return observed_frequencies
    
    @staticmethod
    def generate_intervals(number_generator, intervals_amount, lower_limit, upper_limit, discrete=False):
        if hasattr(number_generator, "lower_limit"):
            lower_limit = number_generator.lower_limit
        intervals = []
        sample_size = upper_limit - lower_limit
        interval_size = sample_size / intervals_amount
        if (discrete):
            interval_size = 1
            lower_limit = lower_limit-1
        partial_lower_limit = lower_limit
        partial_upper_limit = None
        for i in range(intervals_amount):
            partial_upper_limit = partial_lower_limit + interval_size
            if (i+1) == intervals_amount and hasattr(number_generator, "upper_limit"):
                partial_upper_limit = number_generator.upper_limit
            if (i+1) == intervals_amount:
                partial_upper_limit += 0.00001
            if discrete:
                partial_upper_limit = partial_lower_limit + 1
                partial_lower_limit = partial_upper_limit
                
            intervals.append((partial_lower_limit, partial_upper_limit))
            partial_lower_limit = partial_upper_limit
        return intervals

    @staticmethod
    def count_observed_frequency(generated_number, observed_frequencies, is_discrete=False):
        for interval, observed_frequency in observed_frequencies.items():
            lower_limit, upper_limit = interval
            if (not is_discrete and lower_limit <= generated_number and generated_number < upper_limit) or (lower_limit == generated_number):
                expected_freq, counter = observed_frequency
                observed_frequencies[interval] = expected_freq, counter + 1
                break
        return observed_frequencies

    def __init__(
                 self,
                 distribution_generator,
                 history_selector,
                 sample_size,
                 iteration_item_class,
                 intervals_amount=None,
                 discrete=False):
        self.number_generator = distribution_generator
        self.history = []
        self.state_vector = []
        # Expects a function to add elemnts to the history
        self.history_selector = history_selector
        self.iteration_item_class = iteration_item_class
        self.sample_size = int(sample_size)
        self.intervals_amount = intervals_amount
        self.intervals = None
        self.isDiscrete = discrete

    def run(self):
        prev_element = None
        for i in range(self.sample_size):
            if len(self.state_vector) > 0:
                prev_element = self.state_vector[0]
            iteration_number = i + 1
            generated_number = self.number_generator.generate_number()
            parsed_iteration = self.build_iterartion_data(iteration_number, generated_number, prev_element)
            if len(self.state_vector) > 1:
                self.state_vector.pop()
            self.state_vector.insert(0, parsed_iteration)
            history_item = self.history_selector(parsed_iteration)
            if history_item is not None:
                self.history.append(history_item)
        self.frequencies = self.build_observed_frequencies()
        for item in self.history:
            self.frequencies = self.count_observed_frequency(item['generated_number'], self.frequencies, self.isDiscrete)
