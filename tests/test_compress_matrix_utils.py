from datetime import timedelta

import numpy as np
from timeit import default_timer as timer
from src.compression.compress_tree import CompressTree
from src.compression.compress_matrix_utils import matrix_matrix_add, matrix_vector_mult, matrix_matrix_mult


def generate_matrix(k):
    grid_size = 2 ** k
    total_size = grid_size ** 3
    matrix = np.zeros((total_size, total_size), dtype=float)
    for z in range(grid_size):
        for y in range(grid_size):
            for x in range(grid_size):
                current_idx = z * grid_size * grid_size + y * grid_size + x
                neighbors = [(x - 1, y, z), (x + 1, y, z),
                    (x, y - 1, z), (x, y + 1, z),
                    (x, y, z - 1), (x, y, z + 1)]
                for nx, ny, nz in neighbors:
                    if 0 <= nx < grid_size and 0 <= ny < grid_size and 0 <= nz < grid_size:
                        neighbor_idx = nz * grid_size * grid_size + ny * grid_size + nx
                        matrix[current_idx, neighbor_idx] = np.random.random()
    return matrix

def generate_vector(k):
    grid_size = 2 ** k
    total_size = grid_size ** 3
    vector = np.zeros((total_size,1), dtype=float)
    for i in range(total_size):
        vector[i, 0] = np.random.random()
    return vector


def test_matrix_vector_mult():
    matrix = np.array([[6, 2], [5, 4]])
    vector = np.array([[3], [7]])
    expected_result = matrix @ vector
    r = 2
    epsilon = 1e-3
    compressed_tree = CompressTree(matrix, 0, matrix.shape[0], 0, matrix.shape[1])
    compressed_tree.compress(r, epsilon)
    result = matrix_vector_mult(compressed_tree, vector)
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
    result_tree = matrix_matrix_add(compressed_a, compressed_b)
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
    result_tree = matrix_matrix_mult(compressed_tree, compressed_tree)
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

def test_grid_addition():
    matrix_a = generate_matrix(2)
    matrix_b = generate_matrix(2)
    expected_result = matrix_a + matrix_b
    r = 1
    epsilon = 1e-7
    compressed_a = CompressTree(matrix_a, 0, matrix_a.shape[0], 0, matrix_a.shape[1])
    compressed_a.compress(r, epsilon)
    compressed_b = CompressTree(matrix_b, 0, matrix_b.shape[0], 0, matrix_b.shape[1])
    compressed_b.compress(r, epsilon)
    result_tree = matrix_matrix_add(compressed_a, compressed_b)
    decompressed_result = result_tree.decompress()

    for i in range(matrix_a.shape[0]):
        for j in range(matrix_a.shape[1]):
            assert abs(decompressed_result[i, j] - expected_result[i, j]) < 1e-7, "expected_result[i, j] = {}, decompressed_result[i, j] = {}".format(expected_result[i, j], decompressed_result[i, j])
    print("Test passed for matrix_matrix_add")

def test_grid_multiplication():
    matrix_a = generate_matrix(3)
    matrix_b = generate_matrix(3)
    expected_result = matrix_a @ matrix_b
    r = 1
    epsilon = 1e-7
    compressed_a = CompressTree(matrix_a, 0, matrix_a.shape[0], 0, matrix_a.shape[1])
    compressed_a.compress(r, epsilon)
    compressed_b = CompressTree(matrix_b, 0, matrix_b.shape[0], 0, matrix_b.shape[1])
    compressed_b.compress(r, epsilon)
    result_tree = matrix_matrix_mult(compressed_a, compressed_b)
    decompressed_result = result_tree.decompress()

    for i in range(matrix_a.shape[0]):
        for j in range(matrix_b.shape[1]):
            assert abs(decompressed_result[i, j] - expected_result[i, j]) < 1e-7, "expected_result[i, j] = {}, decompressed_result[i, j] = {}".format(expected_result[i, j], decompressed_result[i, j])
    print("Test passed for matrix_matrix_mult")


def time_test_matrix_vector_mult():
    k = 4
    matrix = generate_matrix(k)
    vector = generate_vector(k)
    r = 1
    epsilon = 1e-7
    compressed_matrix = CompressTree(matrix, 0, matrix.shape[0], 0, matrix.shape[1])
    compressed_matrix.compress(r, epsilon)
    print(f"Running compressed matrix by vector multiplication for size: 2^{3*k} x 2^{3*k}")
    start = timer()
    matrix_vector_mult(compressed_matrix, vector)
    end = timer()
    time_elapsed = end - start
    print(f"Time: {timedelta(seconds=time_elapsed)}")
    print(f"Time in seconds: {time_elapsed}")

def time_test_matrix_matrix_mult():
    k = 1
    matrix_a = generate_matrix(k)
    r = 1
    epsilon = 1e-7
    compressed_a = CompressTree(matrix_a, 0, matrix_a.shape[0], 0, matrix_a.shape[1])
    compressed_a.compress(r, epsilon)
    print(f"Running compressed matrix multiplication for size: 2^{3*k} x 2^{3*k}")
    start = timer()
    matrix_matrix_mult(compressed_a, compressed_a)
    end = timer()
    time_elapsed = end - start
    print(f"Time: {timedelta(seconds=time_elapsed)}")
    print(f"Time in seconds: {time_elapsed}")


if __name__ == "__main__":
    time_test_matrix_vector_mult()