from src.calculator import Calculator
from src.algorithms.strassen_algorithm import StrassenAlgorithm
from src.algorithms.Inverse import Inversion
from src.algorithms.binet_algorithm import BinetAlgorithm
import numpy as np

class LUFactorization:
    def __init__(self):
        super().__init__()
        self.calc = Calculator()
        self.strassen = StrassenAlgorithm()
        self.inversion = Inversion()
        binet = BinetAlgorithm()
        self.mul = binet.mul
        self.calcs = (binet.calc,  self.inversion.calc)


    def lu(self, matrix):
        result = self.lu_factorization(matrix)
        #self._update_calculator()
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
            #self.calc += self.inversion.calc



    # def _update_calculator(self):
    #     self.calc += self.mul
    #     self.calc += self.inversion.calc
    #     self.mul.calc.reset_counters()

#
# A = np.array([
#     [0.54, 0.23, 0.67, 0.12, 0.45],
#     [0.78, 0.34, 0.56, 0.91, 0.82],
#     [0.13, 0.58, 0.44, 0.73, 0.27],
#     [0.89, 0.62, 0.35, 0.29, 0.75],
#     [0.48, 0.15, 0.92, 0.64, 0.51]
# ])
# luuu = LUFactorization()
#
# luuu.run(A)
# print("L=")
# print(luuu.L)
#
# print("U=")
# print(luuu.U)
