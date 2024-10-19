from algorithms.example_algorithm import ExampleAlgorithm
from base_algorithm_test import BaseAlgorithmTest


class TestExampleAlgorithm(BaseAlgorithmTest):
    example_algorithm = ExampleAlgorithm()

    def run(self):
        self.generate_data()
        # time start
        self.example_algorithm.run(self.matrix1, self.matrix2)
        # time end

    @classmethod
    def generate_data(cls):
        cls.matrix1 = [[1, 2], [3, 4]]
        cls.matrix2 = [[2, 2], [4, 4]]
