import numpy as np

from src.algorithms.LU import LUFactorization
from src.base_algorithm import BaseAlgorithm


class DetAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.A = None
        self.det = None
        self.lu = LUFactorization()

    def __calculate_determinant(self, A):
        n = A.shape[0]
        if n == 1:
            return A[0, 0]
        _, U = self.lu.lu(A)
        U_diag = np.diagonal(U).tolist()
        k = n
        U_1 = U_diag
        U_2 = []
        while k > 1:
            u_1 = U_1.pop(0)
            u_2 = U_1.pop(-1)
            k -= 2
            U_2.append(u_1 * u_2)
            if k == 1:
                U_2.append(U_1[0])
            if k <= 1 and len(U_2) != 1:
                U_1 = U_2
                U_2 = []
                k = len(U_1)
        return U_2[0]

    def run(self, A):
        n = A.shape[0]
        self.det = self.__calculate_determinant(A)
        self.calc.multiply_count += n
        self.calc.total_count += n
        self.calc += self.lu.calc

    def local_matlab_test(self):
        A = np.array([
            [0.54, 0.23, 0.67, 0.12, 0.45],
            [0.78, 0.34, 0.56, 0.91, 0.82],
            [0.13, 0.58, 0.44, 0.73, 0.27],
            [0.89, 0.62, 0.35, 0.29, 0.75],
            [0.48, 0.15, 0.92, 0.64, 0.51]
        ])
        self.run(A)
        print(self.det)