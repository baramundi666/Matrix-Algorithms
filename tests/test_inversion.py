from random import uniform
from src.algorithms.Inverse import Inversion
from tests.base_algorithm_test import BaseAlgorithmTest
from tests.utils import assert_matrix_inversion_is_correct
import numpy as np

class TestInversion(BaseAlgorithmTest):
    def __init__(self):
        super().__init__()
        self.algorithm = Inversion()
        self.data = {}
        self.n = 500

    def run(self):
        #range_ = range(300, self.n + 1, 50)
        #for test_size in (2**k for k in range(10)):
        #for test_size in range(1, self.n + 1):
        for test_size in range(1, 100):
            self.generate_data(test_size)
            time = self._run_time_test(f"{test_size} x {test_size}", self.matrix)
            flop = self._extract_calc_data()
            self.data[test_size] = {"time": time,
                                    "flop": flop}
            assert_matrix_inversion_is_correct(self.matrix, self.algorithm.matrix_inv)

    @classmethod
    def generate_data(cls, test_size):
        a, b = np.double(0.00000001), np.double(1.0)
        cls.matrix = (b - a) * np.random.rand(test_size, test_size) + a
