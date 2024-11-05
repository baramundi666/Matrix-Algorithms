import numpy as np

from src.algorithms.det_algorithm import DetAlgorithm
from tests.base_algorithm_test import BaseAlgorithmTest
from tests.utils import assert_determinant_is_correct


class TestDetAlgorithm(BaseAlgorithmTest):
    def __init__(self):
        super().__init__()
        self.algorithm = DetAlgorithm()
        self.data = {}
        self.n = 300

    def run(self):
        for test_size in [5]:
            self.generate_data(test_size)
            time = self._run_time_test(f"{test_size} x {test_size}", self.A)
            flop = self._extract_calc_data()
            self.data[test_size] = {"time": time,
                                    "flop": flop}
            assert_determinant_is_correct(self.A,self.algorithm.det)

    @classmethod
    def generate_data(cls, test_size):
        a, b = np.double(0.00000001), np.double(1.0)
        cls.A = (b-a) * np.random.rand(test_size, test_size) + a