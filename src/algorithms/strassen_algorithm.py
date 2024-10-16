from src.base_algorithm import BaseAlgorithm
from src.utils import add, subtract, split_into_block_matrices, multiply_one_by_one_matrices, connect_block_matrices


class StrassenAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.matrix_3 = None

    def run(self, matrix_1, matrix_2):
        """
        matrix_1, matrix_2 - square matrices with size 2^n x 2^n
        """
        matrix_3 = self.__rec(matrix_1, matrix_2)
        self.matrix_3 = matrix_3


    def __rec(self, matrix_1, matrix_2):
        if len(matrix_1) == 1:
            return multiply_one_by_one_matrices(matrix_1, matrix_2)

        matrix_1_11, matrix_1_12, matrix_1_21, matrix_1_22 = split_into_block_matrices(matrix_1)
        matrix_2_11, matrix_2_12, matrix_2_21, matrix_2_22 = split_into_block_matrices(matrix_2)

        p_1 = self.__rec(add(matrix_1_11, matrix_1_22), add(matrix_2_11, matrix_2_22))
        p_2 = self.__rec(add(matrix_1_21, matrix_1_22), matrix_2_11)
        p_3 = self.__rec(matrix_1_11, subtract(matrix_2_12, matrix_2_22))
        p_4 = self.__rec(matrix_1_22, subtract(matrix_2_21, matrix_2_11))
        p_5 = self.__rec(add(matrix_1_11, matrix_1_12), matrix_2_22)
        p_6 = self.__rec(subtract(matrix_1_21, matrix_1_11), add(matrix_2_11, matrix_2_12))
        p_7 = self.__rec(subtract(matrix_1_12, matrix_1_22), add(matrix_2_21, matrix_2_22))

        matrix_3_11 = add(subtract(add(p_1, p_4), p_5), p_7)
        matrix_3_12 = add(p_3, p_5)
        matrix_3_21 = add(p_2, p_4)
        matrix_3_22 = add(add(subtract(p_1, p_2), p_3), p_6)

        matrix_3 = connect_block_matrices(matrix_3_11, matrix_3_12, matrix_3_21, matrix_3_22)
        return matrix_3






