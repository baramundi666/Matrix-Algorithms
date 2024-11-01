import numpy as np

from src.algorithms.LU import LUFactorization
from src.base_algorithm import BaseAlgorithm


class DetAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.A = None
        self.det = None
        self.lu = LUFactorization()

    def run(self, A):
        n = A.shape[0]
        if n == 1:
            self.det = A[0, 0]
            return

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
        self.det = U_2[0]
        self.calc.multiply_count += n
        self.calc.total_count += n
        self.calc += self.lu.calc