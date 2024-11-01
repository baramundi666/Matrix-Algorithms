import numpy as np
import scipy


def assert_matrix_multiplication_is_correct(matrix_1, matrix_2, matrix_3):
    epsilon = 1e-9
    expected_matrix = np.matrix(matrix_1) @ np.matrix(matrix_2)
    actual_matrix = np.matrix(matrix_3)
    n, m = matrix_3.shape
    for i in range(n):
        for j in range(m):
            assert abs(expected_matrix[i,j] - actual_matrix[i,j]) < epsilon, f"Matrix multiplication wasn't successful: expected_matrix[{i},{j}] = {expected_matrix[i,j]} != actual_matrix[{i},{j}] = {actual_matrix[i,j]}"
    print("Matrix multiplication was successful!")

def assert_matrix_inversion_is_correct(matrix, inverse_matrix):
    epsilon = 1e-3
    n = matrix.shape[0]
    expected_inverse_matrix = scipy.linalg.inv(matrix)
    for i in range(n):
        for j in range(n):
            assert abs(expected_inverse_matrix[i, j] - inverse_matrix[i, j]) < epsilon,  f"Matrix inversion wasn't successful: expected_inverse_matrix[{i},{j}] = {expected_inverse_matrix[i,j]} != inverse_matrix[{i},{j}] = {inverse_matrix[i,j]}"
    print("Matrix inversion was successful!")

def assert_lu_factorization_is_correct(matrix, L, U):
    epsilon = 1e-9
    n = matrix.shape[0]
    expected = L @ U
    for i in range(n):
        for j in range(n):
            assert abs(expected[i, j] - matrix[i, j]) < epsilon, f"LU factorization wasn't successful: expected[{i},{j}] = {expected[i,j]} != matrix[{i},{j}] = {matrix[i,j]}"
    print("LU factorization was successful!")

def assert_gauss_elimination_is_correct(expected_A, expected_b, A, b):
    epsilon = 1e-2
    n = len(A)
    expected_x = np.linalg.solve(expected_A, expected_b)
    x = np.linalg.solve(A, b)
    for i in range(n):
        for j in range(i-1, -1, -1):
            assert abs(A[i, j]) < epsilon, f"Error: A[{i}, {j}] = {A[i, j]} != 0"
        assert abs(x[i, 0] - expected_x[i, 0]) < epsilon, f"Error: x[{i}, 0] = {x[i, 0]} != expected_x[{i}, 0] = {expected_x[i, 0]}"
    print("Success!")

def assert_determinant_is_correct(A, det):
    epsilon = 1e-5
    assert abs(det - np.linalg.det(A)) < epsilon, f"Error: det = {det} != expected_det = {np.linalg.det(A)}"
    print("Success!")
