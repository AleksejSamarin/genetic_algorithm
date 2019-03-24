import numpy as np
import random
import math

class GenAlgorithm:

    def __init__(self):
        self.max = 3
        self.min = -3
        self.population_count = 10 # 50 / 4
        self.chromosome_length = 20 # 20 / 5
        self.factor_crossover = 0.5
        self.factor_mutation = 0.15
        self.factor_avoid_zero_probability = 0.001

        self.area = self.max - self.min
        self.chunk_value = self.area / (2**self.chromosome_length - 1)
        self.chromosomes = np.random.randint(2, size=(self.population_count, self.chromosome_length))


    def count_function(self, x):
        return math.cos(1.2 * x - 2) - math.cos(1.7 * x - 1) * math.sin(8.4 * x)


    def run(self):
        for i in range(100):

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
            result_values = self.chromosomes.dot(1 << np.arange(self.chromosomes.shape[-1] - 1, -1, -1)) * self.chunk_value + self.min # start, end (not included), step
            function_values = np.vectorize(self.count_function)(result_values) # apply function to elements

            probabilities_prepare = function_values + np.abs(np.min(function_values)) + self.factor_avoid_zero_probability
            probabilities = probabilities_prepare / np.sum(probabilities_prepare)
            new_population_indices = np.random.choice(probabilities.size, self.population_count, replace=False, p=probabilities)
            self.chromosomes = self.chromosomes[new_population_indices]

        print(self.chromosomes)