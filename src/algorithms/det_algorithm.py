import numpy as np
import scipy

from src.algorithms.Inverse import Inversion
from src.algorithms.LU import LUFactorization
from src.algorithms.binet_algorithm import BinetAlgorithm
from src.base_algorithm import BaseAlgorithm


class DetAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.A = None
        self.det = None
        self.lu = LUFactorization()

    def run(self, A):
        n = A.shape[0]
        L, U = self.lu.lu(A)
        self.det = np.sum(np.diagonal(L) * np.diagonal(U))
        self.calc.multiply_count += n
        self.calc.add_count += n-1
        self.calc.total_count += n + n-1
        self.calc += self.lu.calc