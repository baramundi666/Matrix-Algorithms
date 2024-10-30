import math

from src.base_algorithm import BaseAlgorithm


class BinetAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.matrix_3 = None

    def __binet(self, A, B):
        n = len(A)
        if n == 1:
            return self.calc.standard_matrix_multiplication(A, B)
        if n % 2 == 1:
            A11, A12, A21, A22 = self.calc.split_into_block_matrices_dynamic_peeling(A)
            B11, B12, B21, B22 = self.calc.split_into_block_matrices_dynamic_peeling(B)

            C11 = self.calc.add(self.__binet(A11, B11), self.calc.standard_matrix_multiplication(A12, B21))
            C12 = self.calc.add(self.calc.standard_matrix_multiplication(A11, B12), self.calc.standard_matrix_multiplication(A12, B22))
            C21 = self.calc.add(self.calc.standard_matrix_multiplication(A21, B11), self.calc.standard_matrix_multiplication(A22, B21))
            C22 = self.calc.add(self.calc.standard_matrix_multiplication(A21, B12), self.calc.standard_matrix_multiplication(A22, B22))

            return self.calc.connect_block_matrices_dynamic_peeling(C11, C12, C21, C22)
        else:
            A11, A12, A21, A22 = self.calc.split_into_block_matrices(A)
            B11, B12, B21, B22 = self.calc.split_into_block_matrices(B)

            C11 = self.calc.add(self.__binet(A11, B11), self.__binet(A12, B21))
            C12 = self.calc.add(self.__binet(A11, B12), self.__binet(A12, B22))
            C21 = self.calc.add(self.__binet(A21, B11), self.__binet(A22, B21))
            C22 = self.calc.add(self.__binet(A21, B12), self.__binet(A22, B22))

            return self.calc.connect_block_matrices(C11, C12, C21, C22)

    def run(self, A, B):
        C = self.__binet(A, B)
        self.matrix_3 = C

    def mul(self, A, B):
        n = A.shape[0]
        k = A.shape[1]
        m = B.shape[1]
        if n != k or k != m:
            new_size = max(n, k, m)
            A = self.calc.expand_matrix_to_shape(A, (new_size, new_size))
            B = self.calc.expand_matrix_to_shape(B, (new_size, new_size))
        C = self.__binet(A, B)
        if n != k or k != m:
            C = self.calc.crop_matrix_to_shape(C, (n, m))
        return C