import numpy as np
import random
import math

class GenAlgorithm:

    def __init__(self):
        self.edge_1 = 3
        self.edge_2 = 6
        self.type_length = 20
        self.population_count = 50
        self.factor_crossover = 0.85
        self.factor_mutation = 0.15
        self.iterations = 100
        self.factor_avoid_zero_probability = 0.001


    def count_function(self, x):
        return math.cos(1.2 * x - 2) - math.cos(1.7 * x - 1) * math.sin(8.4 * x)


    def count_function_3d(self, x, y):
        return 0.1 * x + 0.2 * y - 4 * math.cos(x) + 4 * math.cos(0.9 * y) + 5


    def run(self, plot_3d=False):
        self.prepare(plot_3d)
        for i in range(self.iterations):
            np.random.shuffle(self.chromosomes)
            factors_crossover = np.random.rand(int(self.population_count / 2))
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
                    self.chromosomes = np.append(self.chromosomes, children, axis=0)
                    children.clear()
            if self.chromosome_count == 1:
                result_values = self.chromosomes.dot(1 << np.arange(self.chromosomes.shape[-1] - 1, -1, -1)) * self.chunk_value + self.min # start, end (not included), step
                function_values = np.vectorize(self.count_function)(result_values) # apply function to elements
            else:
                reshaped_chromosomes = self.chromosomes.reshape((self.chromosomes.shape[0] * 2, int(self.chromosomes.shape[1] / 2)))
                result_values = reshaped_chromosomes.dot(1 << np.arange(int(self.chromosome_length / 2) - 1, -1, -1)) * self.chunk_value + self.min
                function_values = np.vectorize(self.count_function_3d)(result_values[::2], result_values[1:][::2])

            if plot_3d is False:
                probabilities_prepare = function_values + np.abs(np.min(function_values)) + self.factor_avoid_zero_probability
                probabilities = probabilities_prepare / np.sum(probabilities_prepare)
                new_population_indices = np.random.choice(probabilities.size, self.population_count, replace=False, p=probabilities)
            else:
                flag = True
                new_population_indices = []
                temp = np.copy(function_values)
                while flag:
                    for idx in range(0, temp.size, 2):
                        if len(new_population_indices) < self.population_count:
                            if temp[idx] > temp[idx + 1]:
                                new_population_indices.append(idx)
                            else:
                                new_population_indices.append(idx + 1)
                        else:
                            flag = False
                    np.delete(temp, new_population_indices)

            self.chromosomes = self.chromosomes[new_population_indices]

            if i == 0 or i == 3 or i == self.iterations - 1:
                for idx in range(self.population_count):
                    if plot_3d is False:
                        print(i, idx, '{:0.2f}'.format(result_values[idx]),
                              np.array2string(self.chromosomes[idx], separator=''),
                              '{:0.2f}'.format(function_values[idx], decimals=2), sep='\t')
                    else:
                        print(i, idx, '{:0.2f}'.format(result_values[::2][idx]),
                              '{:0.2f}'.format(result_values[1:][::2][idx]),
                              np.array2string(self.chromosomes[idx], separator=''),
                              np.around(function_values[idx]), sep='\t')

            if self.chromosome_count == 1:
                result_values = self.chromosomes.dot(1 << np.arange(self.chromosomes.shape[-1] - 1, -1, -1)) * self.chunk_value + self.min  # start, end (not included), step
                function_values = np.vectorize(self.count_function)(result_values)
                self.window.update_plot(function_values, result_values)
            else:
                reshaped_chromosomes = self.chromosomes.reshape((self.chromosomes.shape[0] * 2, int(self.chromosomes.shape[1] / 2)))
                result_values = reshaped_chromosomes.dot(1 << np.arange(int(self.chromosome_length / 2) - 1, -1, -1)) * self.chunk_value + self.min
                function_values = np.vectorize(self.count_function_3d)(result_values[::2], result_values[1:][::2])
                self.window.update_plot(function_values, result_values[::2], result_values[1:][::2])


    def prepare(self, plot_3d):
        if plot_3d is True:
            self.chromosome_count = 2
            self.edge = self.edge_2
        else:
            self.chromosome_count = 1
            self.edge = self.edge_1
        self.chromosome_length = self.chromosome_count * self.type_length
        self.chromosomes = np.random.randint(2, size=(self.population_count, self.chromosome_length))
        self.max = self.edge
        self.min = -self.edge
        self.area = self.max - self.min
        self.chunk_value = self.area / (2 ** self.type_length - 1)


    def get_base_data_plot(self, plot_3d=False):
        self.prepare(plot_3d)
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