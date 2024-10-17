from random import uniform

from src.algorithms.ai_algorithm import AIAlgorithm
from tests.base_algorithm_test import BaseAlgorithmTest
from tests.utils import assert_matrix_multiplication_is_correct


class TestAIAlgorithm(BaseAlgorithmTest):
    def __init__(self):
        super().__init__()
        self.algorithm = AIAlgorithm()

    def run(self):
        self.generate_data()
        self._run_time_test("4 x 5, 5 x 5", self.matrix_1, self.matrix_2)
        self._extract_calculator_data()
        assert_matrix_multiplication_is_correct(self.matrix_1, self.matrix_2, self.algorithm.matrix_3)

    @classmethod
    def generate_data(cls):
        cls.matrix_1 = [[0 for _ in range(5)] for _ in range(4)]
        cls.matrix_2 = [[0 for _ in range(5)] for _ in range(5)]
        a, b = 0.00000001, 1.0
        for i in range(4):
            for j in range(5):
                cls.matrix_1[i][j] = uniform(a, b)
        for i in range(5):
            for j in range(5):
                cls.matrix_2[i][j] = uniform(a, b)