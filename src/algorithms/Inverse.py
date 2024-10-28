from src.base_algorithm import BaseAlgorithm
from src.calculator import Calculator
from src.algorithms.strassen_algorithm import StrassenAlgorithm
import numpy as np

class Inversion(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.matrix_3 = None
        self.calculator = Calculator()
        self.strassen = StrassenAlgorithm()


    def inverse(self, matrix):
        result = self.inverse_rec(matrix)
        self._update_calculator()
        return result

    def inverse_rec(self, matrix):
        n = len(matrix)
        if n == 1:
            return self.calculator.inverse_one_by_one_matrix(matrix)

        if n % 2 != 0:
            A11, A12, A21, A22 = self.calculator.split_into_block_matrices_dynamic_peeling(matrix)
        else:
            A11, A12, A21, A22 = self.calculator.split_into_block_matrices(matrix)

        A11_inv = self.inverse_rec(A11)
        S22 = self.calculator.subtract(A22, self.strassen.run(A21, self.strassen.run(A11_inv, A12)))

        if len(S22) == 1 and len(S22[0]) == 1:
            S22_inv = self.calculator.inverse_one_by_one_matrix(S22)
        else:
            S22_inv = self.inverse_rec(S22)

        B11 = self.calculator.add(A11_inv, self.strassen.run(self.strassen.run( self.strassen.run(
                                      self.strassen.run(A11_inv, A12), S22_inv), A21), A11_inv))
        B12 = self.strassen.run(self.strassen.run(self.calculator.negate(A11_inv), A12), S22_inv)
        B21 = self.strassen.run(self.strassen.run(self.calculator.negate(S22_inv), A21), A11_inv)
        B22 = S22_inv

        if n % 2 != 0:
            return self.calculator.connect_block_matrices_dynamic_peeling(B11, B12, B21, B22)
        else:
            return self.calculator.connect_block_matrices(B11, B12, B21, B22)


    def run(self, A):
        self.matrix_3 = self.inverse(A)

    # def inverse_numpy(self, matrix):
    #     matrix = np.array(matrix)
    #     n = len(matrix)
    #     if n == 1:
    #         return np.array([[1 / matrix[0, 0]]])
    #
    #     half_n = n // 2
    #     A11 = matrix[:half_n, :half_n]
    #     A12 = matrix[:half_n, half_n:]
    #     A21 = matrix[half_n:, :half_n]
    #     A22 = matrix[half_n:, half_n:]
    #
    #     A11_inv = self.inverse_numpy(A11)
    #
    #     S22 = A22 - np.linalg.multi_dot([A21, A11_inv, A12])
    #
    #     S22_inv = self.inverse_numpy(S22)
    #
    #     B11 = A11_inv + np.linalg.multi_dot([A11_inv, A12, S22_inv, A21, A11_inv])
    #     B12 = -np.linalg.multi_dot([A11_inv, A12, S22_inv])
    #     B21 = -np.linalg.multi_dot([S22_inv, A21, A11_inv])
    #     B22 = S22_inv
    #
    #
    #     top = np.hstack((B11, B12))
    #     bottom = np.hstack((B21, B22))
    #     A_inv = np.vstack((top, bottom))
    #
    #     return A_inv

    def _update_calculator(self):
        self.calculator += self.strassen.calculator
        self.strassen.calculator.reset_counters()



