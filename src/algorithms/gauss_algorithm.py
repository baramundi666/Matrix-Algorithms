import numpy as np
import scipy

from src.algorithms.Inverse import Inversion
from src.algorithms.LU import LUFactorization
from src.base_algorithm import BaseAlgorithm


class GaussAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.A = None
        self.b = None
        self.lu_algorithm = LUFactorization()
        self.inv_algorithm = Inversion()

    def __rec(self, A, b):
        n = len(A)
        if n == 1:
            return A, b

        A_11, A_12, A_21, A_22 = A[:n // 2, :n // 2], A[:n // 2, n // 2:], A[n // 2:, :n // 2], A[n // 2:, n // 2:]
        b_1, b_2 = b[:n // 2], b[n // 2:]

        # L_11, U_11 = self.lu_algorithm.lu(A_11)
        L_11, U_11 = scipy.linalg.lu(A_11, permute_l=True)

        # L_11_inv = self.inv_algorithm.inverse(L_11)
        # U_11_inv = self.inv_algorithm.inverse(U_11)

        L_11_inv = np.linalg.inv(L_11)
        U_11_inv = np.linalg.inv(U_11)

        tmp = A_21 @ U_11_inv @ L_11_inv
        S = A_22 - tmp @ A_12

        b_1_new = L_11_inv @ b_1
        b_2_new = b_2 - tmp @ b_1

        A_11_new = U_11
        A_12_new = L_11_inv @ A_12
        A_21_new = np.zeros((n // 2, n // 2))
        A_22_new, b_2_new = self.__rec(S, b_2_new)

        top = np.hstack((A_11_new, A_12_new))
        bottom = np.hstack((A_21_new, A_22_new))
        A_new = np.vstack((top, bottom))
        b_new = np.vstack((b_1_new, b_2_new))

        return A_new, b_new


    def run(self, A, b):
        self.A, self.b = self.__rec(A, b)