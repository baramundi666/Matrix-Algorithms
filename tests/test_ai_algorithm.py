from random import uniform

from algorithms.ai_algorithm import AIAlgorithm
from base_algorithm_test import BaseAlgorithmTest
from utils import assert_matrix_multiplication_is_correct


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
            self._run_time_test("4 x 5, 5 x 5", self.matrix_1, self.matrix_2)
            self._extract_calculator_data()
            assert_matrix_multiplication_is_correct(self.matrix_1, self.matrix_2, self.algorithm.matrix_3)

    def generate_data(self, test_shapes):
        n, k, m = test_shapes
        self.matrix_1 = [[0 for _ in range(k)] for _ in range(n)]
        self.matrix_2 = [[0 for _ in range(m)] for _ in range(k)]
        a, b = 0.00000001, 1.0
        for i in range(n):
            for j in range(k):
                self.matrix_1[i][j] = uniform(a, b)
        for i in range(k):
            for j in range(m):
                self.matrix_2[i][j] = uniform(a, b)