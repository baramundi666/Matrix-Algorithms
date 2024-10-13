from random import uniform
from timeit import default_timer as timer
from datetime import timedelta

from src.algorithms.strassen_algorithm import StrassenAlgorithm
from tests.base_algorithm_test import BaseAlgorithmTest
from tests.utils import assert_matrix_multiplication


class TestStrassenAlgorithm(BaseAlgorithmTest):
    strassen_algorithm = StrassenAlgorithm()

    def run(self):
        for test_size in [2**k for k in range(1, 9)]:
            self.generate_data(test_size)
            print(f"Running {self.strassen_algorithm} with testing size: {test_size}")
            # time start
            start = timer()
            # run algorithm
            self.strassen_algorithm.run(self.matrix_1, self.matrix_2)
            # time end
            end = timer()
            print(f"Time: {timedelta(seconds=end - start)}")
            assert_matrix_multiplication(self.matrix_1, self.matrix_2, self.strassen_algorithm.matrix_3)

    @classmethod
    def generate_data(cls, test_size):
        cls.matrix_1 = [[0 for _ in range(test_size)] for _ in range(test_size)]
        cls.matrix_2 = [[0 for _ in range(test_size)] for _ in range(test_size)]
        a, b = 0.00000001, 1.0
        for i in range(test_size):
            for j in range(test_size):
                cls.matrix_1[i][j] = uniform(a, b)
                cls.matrix_2[i][j] = uniform(a, b)

