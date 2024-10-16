import numpy as np


def assert_matrix_multiplication_is_correct(matrix_1, matrix_2, matrix_3):
    epsilon = 1e-9
    expected_matrix = np.matrix(matrix_1) @ np.matrix(matrix_2)
    actual_matrix = np.matrix(matrix_3)
    n = len(matrix_1)
    for i in range(n):
        for j in range(n):
            assert abs(expected_matrix[i,j] - actual_matrix[i,j]) < epsilon, f"Matrix multiplication wasn't successful: expected_matrix[{i},{j}] = {expected_matrix[i,j]} != actual_matrix[{i},{j}] = {actual_matrix[i,j]}"
    print("Matrix multiplication was successful!")