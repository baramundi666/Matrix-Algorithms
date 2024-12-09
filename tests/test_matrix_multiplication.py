import numpy as np
from src.compression.compress_tree import CompressTree
from src.compression.matrix_multiplication import MatrixMultiplication


def test_matrix_vector_mult():
    matrix = np.array([[6, 2], [5, 4]])
    vector = np.array([[3], [7]])
    expected_result = matrix @ vector
    r = 2
    epsilon = 1e-3
    compressed_tree = CompressTree(matrix, 0, matrix.shape[0], 0, matrix.shape[1])
    compressed_tree.compress(r, epsilon)
    result = MatrixMultiplication.matrix_vector_mult(compressed_tree, vector)
    print("matrix_vector_mult")
    print("Matrix:")
    print(matrix)
    print("Vector:")
    print(vector)
    print("Expected Result:")
    print(expected_result)
    print("Compressed Tree Result:")
    print(result)
    assert np.allclose(result, expected_result, atol=1e-3), "Test failed!"
    print("Test passed")


def test_matrix_matrix_add():
    matrix_a = np.array([[5, 3], [2, 4]])
    matrix_b = np.array([[3, 7], [6, 8]])
    expected_result = matrix_a + matrix_b
    r = 1
    epsilon = 1e-3
    compressed_a = CompressTree(matrix_a, 0, matrix_a.shape[0], 0, matrix_a.shape[1])
    compressed_a.compress(r, epsilon)
    compressed_b = CompressTree(matrix_b, 0, matrix_b.shape[0], 0, matrix_b.shape[1])
    compressed_b.compress(r, epsilon)
    result_tree = MatrixMultiplication.matrix_matrix_add(compressed_a, compressed_b)
    decompressed_result = result_tree.decompress()
    print("\nmatrix_matrix_add")
    print("Matrix A:")
    print(matrix_a)
    print("Matrix B:")
    print(matrix_b)
    print("Expected Addition Result:")
    print(expected_result)
    print("Compressed Tree Result (Addition):")
    print(decompressed_result)

    assert np.allclose(decompressed_result, expected_result, atol=1e-3), "Test failed for matrix_matrix_add"
    print("Test passed for matrix_matrix_add")

def test_matrix_matrix_mult():
    matrix = np.array([[13, 4], [2, 7]])
    expected_result = matrix @ matrix
    r = 1
    epsilon = 1e-3
    compressed_tree = CompressTree(matrix, 0, matrix.shape[0], 0, matrix.shape[1])
    compressed_tree.compress(r, epsilon)
    result_tree = MatrixMultiplication.matrix_matrix_mult(compressed_tree, compressed_tree)
    decompressed_result = result_tree.decompress()
    print("\nmatrix_matrix_mult")
    print("Original Matrix:")
    print(matrix)
    print("Expected Result (Matrix @ Matrix):")
    print(expected_result)
    print("Decompressed Result from CompressTree:")
    print(decompressed_result)
    assert np.allclose(decompressed_result, expected_result, atol=1e-3), "Test failed"
    print("Test passed")


if __name__ == "__main__":

    test_matrix_vector_mult()
    test_matrix_matrix_add()
    test_matrix_matrix_mult()