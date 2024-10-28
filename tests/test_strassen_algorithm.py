from random import uniform
from src.algorithms.strassen_algorithm import StrassenAlgorithm
from tests.base_algorithm_test import BaseAlgorithmTest
from tests.utils import assert_matrix_multiplication_is_correct


class TestStrassenAlgorithm(BaseAlgorithmTest):
    def __init__(self):
        super().__init__()
        self.algorithm = StrassenAlgorithm()
        self.data = {}
        self.n = 1000

    def run(self):
        # range_ = range(300, self.n+1, 50)
        for test_size in [33]:
            self.generate_data(test_size)
            time = self._run_time_test(f"{test_size} x {test_size}", self.matrix_1, self.matrix_2)
            flop = self._extract_calculator_data()
            self.data[test_size] = {"time": time,
                                    "flop": flop}
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

