from random import uniform
from src.algorithms.strassen_algorithm import StrassenAlgorithm
from tests.base_algorithm_test import BaseAlgorithmTest
from tests.utils import assert_matrix_multiplication_is_correct


class TestStrassenAlgorithm(BaseAlgorithmTest):
    def __init__(self):
        super().__init__()
        self.algorithm = StrassenAlgorithm()

    def run(self):
        for test_size in [2**k for k in range(1, 5)]:
            self.generate_data(test_size)
            self._run_time_test(test_size, self.matrix_1, self.matrix_2)
            assert_matrix_multiplication_is_correct(self.matrix_1, self.matrix_2, self.algorithm.matrix_3)

    @classmethod
    def generate_data(cls, test_size):
        cls.matrix_1 = [[0 for _ in range(test_size)] for _ in range(test_size)]
        cls.matrix_2 = [[0 for _ in range(test_size)] for _ in range(test_size)]
        a, b = 0.00000001, 1.0
        for i in range(test_size):
            for j in range(test_size):
                cls.matrix_1[i][j] = uniform(a, b)
                cls.matrix_2[i][j] = uniform(a, b)

