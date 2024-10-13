import numpy as np


def assert_matrix_multiplication(matrix_1, matrix_2, matrix_3):
    epsilon = 1e-9
    expected_matrix = np.matrix(matrix_1) @ np.matrix(matrix_2)
    actual_matrix = np.matrix(matrix_3)
    n = len(matrix_1)
    for i in range(n):
        for j in range(n):
            assert abs(expected_matrix[i,j] - actual_matrix[i,j]) < epsilon, f"expected_matrix[{i},{j}] = {expected_matrix[i,j]} != actual_matrix[{i},{j}] = {actual_matrix[i,j]}"