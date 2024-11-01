from src.base_algorithm import BaseAlgorithm
from src.calculator import Calculator
from src.algorithms.binet_algorithm import BinetAlgorithm

class Inversion(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.calc = Calculator()
        self.binet = BinetAlgorithm()
        self.cals = [self.binet.calc]

    def rec_inverse(self, A):
        if A.shape[0] == 1:
            return self.calc.inverse_one_by_one_matrix(A)

        A11, A12, A21, A22 = self.calc.split_into_block_matrices(A)

        A11_inv = self.rec_inverse(A11)

        A11_inv_A12 = self.binet.mul(A11_inv, A12)
        A21_A11_inv = self.binet.mul(A21, A11_inv)
        S = self.calc.subtract(A22, self.binet.mul(A21_A11_inv, A12))

        S_inv = self.rec_inverse(S)

        B11 = self.calc.add(A11_inv, self.binet.mul(self.binet.mul(A11_inv_A12, S_inv), A21_A11_inv))
        B12 = self.calc.negate(self.binet.mul(A11_inv_A12, S_inv))
        B21 = self.calc.negate(self.binet.mul(S_inv, A21_A11_inv))
        B22 = S_inv

        return self.calc.connect_block_matrices(B11, B12, B21, B22)


    def run(self, A):
        self.matrix_3 = self.rec_inverse(A)
        for calc in self.calcs:
            self.calc += calc




#
# A = np.array([
#     [0.54, 0.23, 0.67, 0.12, 0.45],
#     [0.78, 0.34, 0.56, 0.91, 0.82],
#     [0.13, 0.58, 0.44, 0.73, 0.27],
#     [0.89, 0.62, 0.35, 0.29, 0.75],
#     [0.48, 0.15, 0.92, 0.64, 0.51]
# ])
# inv = Inversion()
#
# inv.run(A)
#
# print(inv.matrix_3)



