import numpy as np


def assert_matrix_multiplication_is_correct(matrix_1, matrix_2, matrix_3):
    epsilon = 1e-9
    expected_matrix = np.matrix(matrix_1) @ np.matrix(matrix_2)
    actual_matrix = np.matrix(matrix_3)
    n = len(matrix_3)
    m = len(matrix_3[0])
    for i in range(n):
        for j in range(m):
            assert abs(expected_matrix[i,j] - actual_matrix[i,j]) < epsilon, f"Matrix multiplication wasn't successful: expected_matrix[{i},{j}] = {expected_matrix[i,j]} != actual_matrix[{i},{j}] = {actual_matrix[i,j]}"
    print("Matrix multiplication was successful!")



def assert_matrix_inversion_is_correct(matrix, inverse_matrix, epsilon=1e-1):
    identity_matrix = np.eye(len(matrix))
    product_matrix = np.dot(matrix, inverse_matrix)
    assert np.allclose(product_matrix, identity_matrix, atol=epsilon, rtol=1e-1),  f"Matrix inversion wasn't successful"
    print("Matrix inversion was successful!")



def assert_matrix_inversion(matrix, inverse_matrix, epsilon=1e-1):
    identity_matrix = np.linalg.inv(matrix)
    n = len(matrix)
    m = len(matrix[0])
    for i in range(n):
        for j in range(m):
            assert abs(inverse_matrix[i][j] - identity_matrix[
                i][j]) < epsilon, f"Matrix inversion wasn't successful"
    print("Matrix inversion was successful!")


def assert_lu_factorization_is_correct(matrix, L, U, epsilon=1e-9):
    matrix_np = np.array(matrix)
    L_np = np.array(L)
    U_np = np.array(U)
    product_matrix = np.dot(L_np, U_np)
    assert np.allclose(product_matrix, matrix_np, atol=epsilon, rtol=1e-9), f"LU factorization wasn't successful: "
    print("LU factorization was successful!")

def assert_gauss_elimination_is_correct(expected_A, expected_b, A, b):
    epsilon = 1e-9
    n = len(A)
    expected_x = np.linalg.solve(expected_A, expected_b)
    x = np.linalg.solve(A, b)
    for i in range(n):
        for j in range(i-1, -1, -1):
            assert abs(A[i, j]) < epsilon, f"Error: A[{i}, {j}] = {A[i, j]} != 0"
        assert abs(x[i, 0] - expected_x[i, 0]) < epsilon, f"Error: x[{i}, 0] = {x[i, 0]} != expected_x[{i}, 0] = {expected_x[i, 0]}"
    print("Success!")

def assert_determinant_is_correct(A, det):
    epsilon = 1e-9
    assert abs(det - np.linalg.det(A)) < epsilon, f"Error: det = {det} != expected_det = {np.linalg.det(A)}"
    print("Success!")