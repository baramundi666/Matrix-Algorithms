import math
from src.base_algorithm import BaseAlgorithm

class StrassenAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.matrix_3 = None

    def run(self, matrix_1, matrix_2):
        n = max(len(matrix_1), len(matrix_1[0]), len(matrix_2), len(matrix_2[0]))
        n_ = 2 ** int(math.ceil(math.log2(n)))

        matrix_1_expanded = self.calculator.expand_matrix_to_shape(matrix_1, (n_, n_))
        matrix_2_expanded = self.calculator.expand_matrix_to_shape(matrix_2, (n_, n_))

        result = self.__rec(matrix_1_expanded, matrix_2_expanded)
        self.matrix_3 = self.calculator.crop_matrix_to_shape(result, (len(matrix_1), len(matrix_2[0])))
        return self.matrix_3


    def __rec(self, matrix_1, matrix_2):
        if len(matrix_1) == 1:
            return self.calculator.multiply_one_by_one_matrices(matrix_1, matrix_2)

        A11, A12, A21, A22 = self.calculator.split_into_block_matrices(matrix_1)
        B11, B12, B21, B22 = self.calculator.split_into_block_matrices(matrix_2)

        P1 = self.__rec(self.calculator.add(A11, A22), self.calculator.add(B11, B22))
        P2 = self.__rec(self.calculator.add(A21, A22), B11)
        P3 = self.__rec(A11, self.calculator.subtract(B12, B22))
        P4 = self.__rec(A22, self.calculator.subtract(B21, B11))
        P5 = self.__rec(self.calculator.add(A11, A12), B22)
        P6 = self.__rec(self.calculator.subtract(A21, A11), self.calculator.add(B11, B12))
        P7 = self.__rec(self.calculator.subtract(A12, A22), self.calculator.add(B21, B22))

        C11 = self.calculator.add(self.calculator.subtract(self.calculator.add(P1, P4), P5), P7)
        C12 = self.calculator.add(P3, P5)
        C21 = self.calculator.add(P2, P4)
        C22 = self.calculator.add(self.calculator.subtract(self.calculator.add(P1, P3), P2), P6)

        return self.calculator.connect_block_matrices(C11, C12, C21, C22)