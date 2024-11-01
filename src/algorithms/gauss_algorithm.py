import numpy as np

from src.algorithms.Inverse import Inversion
from src.algorithms.LU import LUFactorization
from src.algorithms.binet_algorithm import BinetAlgorithm
from src.base_algorithm import BaseAlgorithm


class GaussAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.A = None
        self.b = None
        self.lu = LUFactorization()
        self.inv = Inversion()
        binet = BinetAlgorithm()
        self.mul = binet.mul
        self.calcs = [binet.calc, self.lu.calc, self.inv.calc]

    def __rec(self, A, b):
        n = len(A)
        if n == 1:
            return A, b

        n_half = n // 2
        A_11, A_12, A_21, A_22 = self.calc.split_into_block_matrices(A)
        b_1, b_2 = self.calc.split_into_block_vectors(b)

        L_11, U_11 = self.lu.lu(A_11)

        L_11_inv = self.inv.inverse(L_11)
        U_11_inv = self.inv.inverse(U_11)

        tmp = self.mul(self.mul(A_21, U_11_inv), L_11_inv)
        S = self.calc.subtract(A_22, self.mul(tmp, A_12))

        L_S, U_S = self.lu.lu(S)
        L_S_inv = self.inv.inverse(L_S)

        b_1_new = self.mul(L_11_inv, b_1)
        # b_2_new = self.calc.subtract(b_2, self.mul(tmp, b_1))
        b_2_new = self.calc.subtract(self.mul(L_S_inv, b_2), self.mul(L_S_inv, self.mul(tmp, b_1)))

        A_11_new = U_11
        A_12_new = self.mul(L_11_inv, A_12)
        A_21_new = np.zeros((n-n_half, n_half))
        # A_22_new, b_2_new = self.__rec(S, b_2_new)
        A_22_new, b_2_new = self.__rec(U_S, b_2_new)

        A_new = self.calc.connect_block_matrices(A_11_new, A_12_new, A_21_new, A_22_new)
        b_new = self.calc.connect_block_vectors(b_1_new, b_2_new)

        return A_new, b_new


    def run(self, A, b):
        self.A, self.b = self.__rec(A, b)
        for calc in self.calcs:
            self.calc += calc