from random import uniform
from src.algorithms.LU import LUFactorization
from tests.base_algorithm_test import BaseAlgorithmTest
from tests.utils import assert_lu_factorization_is_correct
import numpy as np

class TestLU(BaseAlgorithmTest):
    def __init__(self):
        super().__init__()
        self.algorithm = LUFactorization()
        self.data = {}
        self.n = 55



    def run(self):
        #for test_size in range(800, self.n + 1, 25):
        for test_size in range(50, self.n + 1):
        #for test_size in [55]:
            self.generate_data(test_size)
            time = self._run_time_test(f"{test_size} x {test_size}", self.matrix_1)
            flop = self._extract_calculator_data()
            self.data[test_size] = {"time": time,
                                    "flop": flop}
            assert_lu_factorization_is_correct(self.matrix_1, self.algorithm.L, self.algorithm.U)

    @classmethod
    def generate_data(cls, test_size):
        a, b = np.double(0.00000001), np.double(1.0)
        cls.matrix_1 = (b - a) * np.random.rand(test_size, test_size) + a

