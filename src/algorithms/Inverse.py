from src.base_algorithm import BaseAlgorithm
from src.calculator import Calculator
from src.algorithms.binet_algorithm import BinetAlgorithm

class Inversion(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.calc = Calculator()
        self.binet = BinetAlgorithm()
        self.cals = [self.binet.calc]

    def invert(self, A):
        if A.shape[0] == 1:
            return self.calc.inverse_one_by_one_matrix(A)

        A11, A12, A21, A22 = self.calc.split_into_block_matrices(A)

        A11_inv = self.invert(A11)

        A11_inv_A12 = self.binet.mul(A11_inv, A12)
        A21_A11_inv = self.binet.mul(A21, A11_inv)
        S = self.calc.subtract(A22, self.binet.mul(A21_A11_inv, A12))

        S_inv = self.invert(S)

        upper_left = self.calc.add(A11_inv, self.binet.mul(self.binet.mul(A11_inv_A12, S_inv), A21_A11_inv))
        upper_right = self.calc.negate(self.binet.mul(A11_inv_A12, S_inv))
        lower_left = self.calc.negate(self.binet.mul(S_inv, A21_A11_inv))
        lower_right = S_inv


        return self.calc.connect_block_matrices(upper_left, upper_right, lower_left, lower_right)


    def run(self, A):
        self.matrix_3 = self.invert(A)
        for calc in self.calcs:
            self.calc += calc

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




