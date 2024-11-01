import numpy as np


class Calculator:
    def __init__(self):
        self.total_count = 0
        self.add_count = 0
        self.subtract_count = 0
        self.negate_count = 0
        self.multiply_count = 0
        self.divide_count = 0

    def reset_counters(self):
        self.total_count = 0
        self.add_count = 0
        self.subtract_count = 0
        self.negate_count = 0
        self.multiply_count = 0
        self.divide_count = 0

    def add(self, matrix_1, matrix_2):
        n, m = matrix_1.shape
        self.total_count += n * m
        self.add_count += n * m

        return np.add(matrix_1, matrix_2)

    def subtract(self, matrix_1, matrix_2):
        n, m = matrix_1.shape
        self.total_count += n * m
        self.subtract_count += n * m

        return np.subtract(matrix_1, matrix_2)

    def negate(self, matrix):
        n, m = matrix.shape
        self.total_count += n * m
        self.subtract_count += n * m
        return -matrix

    def inverse_one_by_one_matrix(self, matrix):
        self.total_count += 1
        self.divide_count += 1
        return np.array([[1 / matrix[0, 0]]])

    def split_into_block_matrices(self, A):
        n = A.shape[0]
        n_half = n // 2
        A_11, A_12, A_21, A_22 = (A[:n_half, :n_half], A[:n_half, n_half:],
                                  A[n_half:, :n_half], A[n_half:, n_half:])
        return A_11, A_12, A_21, A_22

    def split_into_block_vectors(self, b):
        n = len(b)
        n_half = n // 2
        b_1, b_2 = b[:n_half], b[n_half:]
        return b_1, b_2

    def connect_block_matrices(self, A_11, A_12, A_21, A_22):
        top = np.concatenate((A_11, A_12), axis=1)
        bottom = np.concatenate((A_21, A_22), axis=1)
        A = np.concatenate((top, bottom), axis=0)
        return A

    def connect_block_vectors(self, b_1, b_2):
        b = np.concatenate((b_1, b_2), axis=0)
        return b

    def split_into_block_matrices_dynamic_peeling(self, A):
        n = len(A)
        A_11, A_12, A_21, A_22 = (A[:n-1, :n-1], A[:n-1, n-1:],
                                  A[n-1:, :n-1], A[n-1:, n-1:])
        return A_11, A_12, A_21, A_22

    def connect_block_matrices_dynamic_peeling(self, matrix_11, matrix_12, matrix_21, matrix_22):
        return self.connect_block_matrices(matrix_11, matrix_12, matrix_21, matrix_22)


    def standard_matrix_multiplication(self, matrix_1, matrix_2):
        assert len(matrix_1[0]) == len(matrix_2), "Wrong shapes"
        n = len(matrix_1)
        k = len(matrix_1[0])
        m = len(matrix_2[0])
        matrix = matrix_1 @ matrix_2
        self.add_count += n * (k-1) * m
        self.multiply_count += n * k * m
        self.total_count += n * (k-1) * m + n * k * m
        return matrix

    def crop_matrix_to_shape(self, matrix, shape):
        return matrix[:shape[0], :shape[1]]

    def expand_matrix_to_shape(self, A, shape):
        n = len(A)
        m = len(A[0])
        return np.pad(A, ((0, shape[0] - n), (0, shape[1] - m)), mode='constant')

    def __add__(self, other):
        assert isinstance(other, Calculator)
        new = Calculator()
        new.total_count = self.total_count + other.total_count
        new.add_count = self.add_count + other.add_count
        new.subtract_count = self.subtract_count + other.subtract_count
        new.negate_count = self.negate_count + other.negate_count
        new.multiply_count = self.multiply_count + other.multiply_count
        new.divide_count = self.divide_count + other.divide_count
        return new
