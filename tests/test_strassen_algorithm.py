from random import uniform

import numpy as np

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
        for test_size in [100]:
            self.generate_data(test_size)
            time = self._run_time_test(f"{test_size} x {test_size}", self.matrix_1, self.matrix_2)
            flop = self._extract_calc_data()
            self.data[test_size] = {"time": time,
                                    "flop": flop}
            assert_matrix_multiplication_is_correct(self.matrix_1, self.matrix_2, self.algorithm.matrix_3)

    @classmethod
    def generate_data(cls, test_size):
        a, b = np.double(0.00000001), np.double(1.0)
        cls.matrix_1 = (b - a) * np.random.rand(test_size, test_size) + a
        cls.matrix_2 = (b - a) * np.random.rand(test_size, test_size) + a

