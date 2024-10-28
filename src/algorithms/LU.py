from src.calculator import Calculator
from src.algorithms.strassen_algorithm import StrassenAlgorithm
from src.algorithms.Inverse import Inversion


class LUFactorization:
    def __init__(self):
        self.calculator = Calculator()
        self.strassen = StrassenAlgorithm()
        self.inversion = Inversion()


    def lu(self, matrix):
        result = self.lu_recursive(matrix)
        self._update_calculator()
        return result

    def lu_recursive(self, matrix):
        n = len(matrix)

        if n == 1:
            return [[1]], [[matrix[0][0]]]

        if n % 2 == 0:
            A11, A12, A21, A22 = self.calculator.split_into_block_matrices(matrix)
        else:
            A11, A12, A21, A22 = self.calculator.split_into_block_matrices_dynamic_peeling(matrix)

        L11, U11 = self.lu_recursive(A11)

        U11_inv = self.inversion.inverse(U11)
        L11_inv = self.inversion.inverse(L11)

        L21 = self.strassen.run(A21, U11_inv)
        U12 = self.strassen.run(L11_inv, A12)
        S = self.calculator.subtract(A22, self.strassen.run(L21, U12))

        Ls, Us = self.lu_recursive(S)

        if n % 2 == 0:
            L = self.calculator.connect_block_matrices(L11, [[0] * len(U12[0])] * len(L11), L21, Ls)
            U = self.calculator.connect_block_matrices(U11, U12, [[0] * len(L21[0])] * len(U11), Us)
        else:
            L = self.calculator.connect_block_matrices_dynamic_peeling(L11, [[0] * len(U12[0])] * len(L11), L21, Ls)
            U = self.calculator.connect_block_matrices_dynamic_peeling(U11, U12, [[0] * len(L21[0])] * len(U11), Us)

        return L, U

    def run(self, matrix):

        self.L, self.U = self.lu(matrix)


    def _update_calculator(self):
        self.calculator += self.strassen.calculator
        self.calculator += self.inversion.calculator
        self.strassen.calculator.reset_counters()


