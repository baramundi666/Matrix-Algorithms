from src.base_algorithm import BaseAlgorithm
from src.calculator import Calculator
from src.algorithms.strassen_algorithm import StrassenAlgorithm
from src.algorithms.Inverse import Inversion
from src.algorithms.binet_algorithm import BinetAlgorithm
import numpy as np

class LUFactorization(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.strassen = StrassenAlgorithm()
        self.inversion = Inversion()
        binet = BinetAlgorithm()
        self.mul = binet.mul
        self.calcs = [binet.calc,  self.inversion.calc]


    def lu(self, matrix):
        result = self.lu_factorization(matrix)
        return result

    def lu_factorization(self, A):
        n = len(A)

        if n == 1:
            L = np.array([[1]])
            U = np.array([[A[0, 0]]])
            return L, U

        A11, A12, A21, A22 = self.calc.split_into_block_matrices(A)

        L11, U11 = self.lu_factorization(A11)

        L21 = self.mul(A21, self.inversion.inverse(U11))
        U12 = self.mul(self.inversion.inverse(L11), A12)

        S = self.calc.subtract(A22, self.mul(L21, U12))

        L22, U22 = self.lu_factorization(S)

        L_top = np.hstack((L11, np.zeros_like(U12)))
        L_bottom = np.hstack((L21, L22))
        L = np.vstack((L_top, L_bottom))

        U_top = np.hstack((U11, U12))
        U_bottom = np.hstack((np.zeros_like(L21), U22))
        U = np.vstack((U_top, U_bottom))

        return L, U

    def run(self, matrix):
        self.L, self.U = self.lu(matrix)
        for calc in self.calcs:
            self.calc += calc


