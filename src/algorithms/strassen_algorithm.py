import math

from src.base_algorithm import BaseAlgorithm


class StrassenAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.matrix_3 = None

    def run(self, matrix_1, matrix_2):
        """
        matrix_1, matrix_2 - square matrices with size 2^n x 2^n
        """
        n = len(matrix_1)
        n_ = 2 ** math.ceil(math.log(n, 2))
        matrix_1 = self.calculator.expand_matrix_to_shape(matrix_1, (n_, n_))
        matrix_2 = self.calculator.expand_matrix_to_shape(matrix_2, (n_, n_))
        matrix_3 = self.__rec(matrix_1, matrix_2)
        self.matrix_3 = self.calculator.crop_matrix_to_shape(matrix_3, (n, n))


    def __rec(self, matrix_1, matrix_2):
        if len(matrix_1) == 1:
            return self.calculator.multiply_one_by_one_matrices(matrix_1, matrix_2)

        matrix_1_11, matrix_1_12, matrix_1_21, matrix_1_22 = self.calculator.split_into_block_matrices(matrix_1)
        matrix_2_11, matrix_2_12, matrix_2_21, matrix_2_22 = self.calculator.split_into_block_matrices(matrix_2)

        p_1 = self.__rec(self.calculator.add(matrix_1_11, matrix_1_22), self.calculator.add(matrix_2_11, matrix_2_22))
        p_2 = self.__rec(self.calculator.add(matrix_1_21, matrix_1_22), matrix_2_11)
        p_3 = self.__rec(matrix_1_11, self.calculator.subtract(matrix_2_12, matrix_2_22))
        p_4 = self.__rec(matrix_1_22, self.calculator.subtract(matrix_2_21, matrix_2_11))
        p_5 = self.__rec(self.calculator.add(matrix_1_11, matrix_1_12), matrix_2_22)
        p_6 = self.__rec(self.calculator.subtract(matrix_1_21, matrix_1_11), self.calculator.add(matrix_2_11, matrix_2_12))
        p_7 = self.__rec(self.calculator.subtract(matrix_1_12, matrix_1_22), self.calculator.add(matrix_2_21, matrix_2_22))

        matrix_3_11 = self.calculator.add(self.calculator.subtract(self.calculator.add(p_1, p_4), p_5), p_7)
        matrix_3_12 = self.calculator.add(p_3, p_5)
        matrix_3_21 = self.calculator.add(p_2, p_4)
        matrix_3_22 = self.calculator.add(self.calculator.add(self.calculator.subtract(p_1, p_2), p_3), p_6)

        matrix_3 = self.calculator.connect_block_matrices(matrix_3_11, matrix_3_12, matrix_3_21, matrix_3_22)
        return matrix_3






