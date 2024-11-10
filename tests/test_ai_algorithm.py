from random import uniform

from src.algorithms.ai_algorithm import AIAlgorithm
from tests.base_algorithm_test import BaseAlgorithmTest
from tests.utils import assert_matrix_multiplication_is_correct


class TestAIAlgorithm(BaseAlgorithmTest):
    def __init__(self):
        super().__init__()
        self.algorithm = AIAlgorithm()

    def run(self):
        shapes = [
            (4, 5, 5),
            (16, 5, 25),
            (16, 25, 125),
            (13, 29, 63)
        ]

        for shape in shapes:
            self.generate_data(shape)
            self._run_time_test(f"{shape[0]} x {shape[1]}, {shape[1]} x {shape[2]}", self.matrix_1, self.matrix_2)
            self._extract_calc_data()
            assert_matrix_multiplication_is_correct(self.matrix_1, self.matrix_2, self.algorithm.matrix_3)

    @classmethod
    def generate_data(cls, test_shapes):
        n, k, m = test_shapes
        cls.matrix_1 = [[0 for _ in range(k)] for _ in range(n)]
        cls.matrix_2 = [[0 for _ in range(m)] for _ in range(k)]
        a, b = 0.00000001, 1.0
        for i in range(n):
            for j in range(k):
                cls.matrix_1[i][j] = uniform(a, b)
        for i in range(k):
            for j in range(m):
                cls.matrix_2[i][j] = uniform(a, b)