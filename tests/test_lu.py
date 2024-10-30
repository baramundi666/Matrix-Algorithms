from random import uniform
from src.algorithms.LU import LUFactorization
from tests.base_algorithm_test import BaseAlgorithmTest
from tests.utils import assert_lu_factorization_is_correct

class TestLU(BaseAlgorithmTest):
    def __init__(self):
        super().__init__()
        self.algorithm = LUFactorization()
        self.data = {}



    def run(self):
        for test_size in [10]:
            self.generate_data(test_size)
            time = self._run_time_test(f"{test_size} x {test_size}", self.matrix)
            flop = self._extract_calc_data()
            self.data[test_size] = {"time": time,
                                    "flop": flop}
            assert_lu_factorization_is_correct(self.matrix, self.algorithm.L, self.algorithm.U)

    @classmethod
    def generate_data(cls, test_size):


        cls.matrix = [[0 for _ in range(test_size)] for _ in range(test_size)]

        a, b = 0.00000001, 1.0
        for i in range(test_size):
            for j in range(test_size):
                cls.matrix[i][j] = uniform(a, b)

