import numpy as np
import random
import math

class GenAlgorithm:

    def __init__(self):
        self.max = 3
        self.min = -3
        self.type_length = 20 # 20 / 5
        self.population_count = 50 # 50 / 4
        self.factor_crossover = 0.5
        self.factor_mutation = 0.15
        self.iterations = 100

        self.factor_avoid_zero_probability = 0.001
        self.area = self.max - self.min
        self.chunk_value = self.area / (2 ** self.type_length - 1)


    def count_function(self, x):
        return math.cos(1.2 * x - 2) - math.cos(1.7 * x - 1) * math.sin(8.4 * x)


    def count_function_3d(self, x, y):
        return 0.1 * x + 0.2 * y - 4 * math.cos(x) + 4 * math.cos(0.9 * y) + 5


    def run(self, count):
        self.prepare(count)
        for i in range(self.iterations):
            np.random.shuffle(self.chromosomes)
            factors_crossover = np.random.rand(int(self.population_count / 2))
            # print(factors_crossover)
            children = []
            for idx in range(0, self.population_count, 2):
                if factors_crossover[int(idx / 2)] < self.factor_crossover:
                    crossover_location = random.randint(1, self.chromosome_length - 1)
                    children.append(np.concatenate((self.chromosomes[idx][:crossover_location], self.chromosomes[idx + 1][crossover_location:])))
                    children.append(np.concatenate((self.chromosomes[idx + 1][:crossover_location], self.chromosomes[idx][crossover_location:])))
                    factors_mutation = np.random.rand(2)
                    for index, child in enumerate(children):
                        if factors_mutation[index] < self.factor_mutation:
                            child[random.randint(0, self.chromosome_length - 1)] ^= 1
                    # print(crossover_location, children)
                    self.chromosomes = np.append(self.chromosomes, children, axis=0)
                    children.clear()
            # print(chromosomes)
            if self.chromosome_count == 1:
                result_values = self.chromosomes.dot(1 << np.arange(self.chromosomes.shape[-1] - 1, -1, -1)) * self.chunk_value + self.min # start, end (not included), step
                function_values = np.vectorize(self.count_function)(result_values) # apply function to elements
            else:
                reshaped_chromosomes = self.chromosomes.reshape((self.chromosomes.shape[0] * 2, int(self.chromosomes.shape[1] / 2)))
                result_values = reshaped_chromosomes.dot(1 << np.arange(int(self.chromosome_length / 2) - 1, -1, -1)) * self.chunk_value + self.min
                function_values = np.vectorize(self.count_function_3d)(result_values[::2], result_values[1:][::2])
                # print(self.chromosomes, result_values, function_values, sep='\n')

            probabilities_prepare = function_values + np.abs(np.min(function_values)) + self.factor_avoid_zero_probability
            probabilities = probabilities_prepare / np.sum(probabilities_prepare)
            new_population_indices = np.random.choice(probabilities.size, self.population_count, replace=False, p=probabilities)
            self.chromosomes = self.chromosomes[new_population_indices]

            if self.chromosome_count == 1:
                result_values = self.chromosomes.dot(1 << np.arange(self.chromosomes.shape[-1] - 1, -1, -1)) * self.chunk_value + self.min  # start, end (not included), step
                function_values = np.vectorize(self.count_function)(result_values)
                self.window.update_plot(function_values, result_values)
            else:
                reshaped_chromosomes = self.chromosomes.reshape((self.chromosomes.shape[0] * 2, int(self.chromosomes.shape[1] / 2)))
                result_values = reshaped_chromosomes.dot(1 << np.arange(int(self.chromosome_length / 2) - 1, -1, -1)) * self.chunk_value + self.min
                function_values = np.vectorize(self.count_function_3d)(result_values[::2], result_values[1:][::2])
                self.window.update_plot(function_values, result_values[::2], result_values[1:][::2])
        # print(self.chromosomes)


    def prepare(self, count):
        self.chromosome_count = count
        self.chromosome_length = self.chromosome_count * self.type_length
        self.chromosomes = np.random.randint(2, size=(self.population_count, self.chromosome_length))


    def get_base_data_plot(self, plot_3d=False):
        x = np.arange(self.min, self.max, self.area / (self.population_count * 2))
        if plot_3d is True:
            y = np.copy(x)
            x, y = np.meshgrid(x, y)
            results = np.vectorize(self.count_function_3d)(x, y)
            return x, y, results
        results = np.vectorize(self.count_function)(x)
        return x, results


    def set_window(self, window):
        self.window = window