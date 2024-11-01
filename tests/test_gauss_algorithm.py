import numpy as np

from src.algorithms.gauss_algorithm import GaussAlgorithm
from tests.base_algorithm_test import BaseAlgorithmTest
from tests.utils import assert_gauss_elimination_is_correct


class TestGaussAlgorithm(BaseAlgorithmTest):
    def __init__(self):
        super().__init__()
        self.algorithm = GaussAlgorithm()
        self.data = {}

    def run(self):
        for test_size in [500]:
            self.generate_data(test_size)
            time = self._run_time_test(f"{test_size} x {test_size}", self.A, self.b)
            flop = self._extract_calc_data()
            self.data[test_size] = {"time": time,
                                    "flop": flop}
            assert_gauss_elimination_is_correct(self.A, self.b, self.algorithm.A, self.algorithm.b)

    @classmethod
    def generate_data(cls, test_size):
        a, b = np.double(0.00000001), np.double(1.0)
        cls.A = (b-a) * np.random.rand(test_size, test_size) + a
        cls.b = (b-a) * np.random.rand(test_size, 1) + a