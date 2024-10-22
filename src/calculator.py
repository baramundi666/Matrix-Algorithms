class Calculator:
    def __init__(self):
        self.total_count = 0
        self.add_count = 0
        self.subtract_count = 0
        self.negate_count = 0
        self.multiply_count = 0

    def reset_counters(self):
        self.total_count = 0
        self.add_count = 0
        self.subtract_count = 0
        self.negate_count = 0
        self.multiply_count = 0

    def add(self, matrix_1, matrix_2):
        n = len(matrix_1)
        m = len(matrix_1[0])
        matrix_3 = [[0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                # atomic addition
                self.total_count += 1
                self.add_count += 1
                matrix_3[i][j] = matrix_1[i][j] + matrix_2[i][j]
        return matrix_3

    def subtract(self, matrix_1, matrix_2):
        n = len(matrix_1)
        m = len(matrix_1[0])
        matrix_3 = [[0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                # atomic subtraction
                self.total_count += 1
                self.subtract_count += 1
                matrix_3[i][j] = matrix_1[i][j] - matrix_2[i][j]
        return matrix_3

    def negate(self, matrix):
        n = len(matrix)
        m = len(matrix[0])
        matrix_ = [[0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                # atomic negation
                self.total_count += 1
                self.negate_count += 1
                matrix_[i][j] = -matrix[i][j]
        return matrix_

    def multiply_one_by_one_matrices(self, matrix_1, matrix_2):
        # atomic multiplication
        self.total_count += 1
        self.multiply_count += 1
        matrix_3 = [[matrix_1[0][0] * matrix_2[0][0]]]
        return matrix_3

    def split_into_block_matrices(self, matrix):
        n = len(matrix)
        matrix_11 = [[0 for _ in range(n // 2)] for _ in range(n // 2)]
        matrix_12 = [[0 for _ in range(n // 2)] for _ in range(n // 2)]
        matrix_21 = [[0 for _ in range(n // 2)] for _ in range(n // 2)]
        matrix_22 = [[0 for _ in range(n // 2)] for _ in range(n // 2)]
        for i in range(n):
            for j in range(n):
                if i < n // 2 and j < n // 2:
                    matrix_11[i][j] = matrix[i][j]
                elif i < n // 2 and j >= n // 2:
                    matrix_12[i][j - n // 2] = matrix[i][j]
                elif i >= n // 2 and j < n // 2:
                    matrix_21[i - n // 2][j] = matrix[i][j]
                elif i >= n // 2 and j >= n // 2:
                    matrix_22[i - n // 2][j - n // 2] = matrix[i][j]
        return matrix_11, matrix_12, matrix_21, matrix_22

    def connect_block_matrices(self, matrix_11, matrix_12, matrix_21, matrix_22):
        n = len(matrix_11)
        matrix = [[0 for _ in range(2 * n)] for _ in range(2 * n)]
        for i in range(2 * n):
            for j in range(2 * n):
                if i < n and j < n:
                    matrix[i][j] = matrix_11[i][j]
                elif i < n and j >= n:
                    matrix[i][j] = matrix_12[i][j - n]
                elif i >= n and j < n:
                    matrix[i][j] = matrix_21[i - n][j]
                elif i >= n and j >= n:
                    matrix[i][j] = matrix_22[i - n][j - n]
        return matrix

    def split_into_block_matrices_dynamic_peeling(self, matrix):
        n = len(matrix)
        matrix_11 = [[0 for _ in range(n-1)] for _ in range(n-1)]
        matrix_12 = [[0 for _ in range(1)] for _ in range(n-1)]
        matrix_21 = [[0 for _ in range(n-1)] for _ in range(1)]
        matrix_22 = [[0 for _ in range(1)] for _ in range(1)]
        for i in range(n):
            for j in range(n):
                if i < n-1 and j < n-1:
                    matrix_11[i][j] = matrix[i][j]
                elif i < n-1 and j >= n-1:
                    matrix_12[i][j - n + 1] = matrix[i][j]
                elif i >= n-1 and j < n-1:
                    matrix_21[i - n + 1][j] = matrix[i][j]
                elif i >= n-1 and j >= n-1:
                    matrix_22[i - n + 1][j - n + 1] = matrix[i][j]
        return matrix_11, matrix_12, matrix_21, matrix_22

    def connect_block_matrices_dynamic_peeling(self, matrix_11, matrix_12, matrix_21, matrix_22):
        n = len(matrix_11)
        matrix = [[0 for _ in range(n+1)] for _ in range(n+1)]
        for i in range(n+1):
            for j in range(n+1):
                if i < n and j < n:
                    matrix[i][j] = matrix_11[i][j]
                elif i < n and j >= n:
                    matrix[i][j] = matrix_12[i][j - n]
                elif i >= n and j < n:
                    matrix[i][j] = matrix_21[i - n][j]
                elif i >= n and j >= n:
                    matrix[i][j] = matrix_22[i - n][j - n]
        return matrix


    def standard_matrix_multiplication(self, matrix_1, matrix_2):
        assert len(matrix_1[0]) == len(matrix_2), "Wrong shapes"
        n = len(matrix_1)
        k = len(matrix_1[0])
        m = len(matrix_2[0])
        matrix = [[0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                matrix[i][j] = sum(matrix_1[i][s] * matrix_2[s][j] for s in range(k))
        self.add_count += n * (k-1) * m
        self.multiply_count += n * k * m

        return matrix

    def crop_matrix_to_shape(self, matrix, shape):
        matrix_ = [[matrix[i][j] for j in range(shape[1])] for i in range(shape[0])]
        return matrix_

    def expand_matrix_to_shape(self, matrix, shape):
        n = len(matrix)
        m = len(matrix[0])
        matrix_ = [[0 for _ in range(shape[1])] for _ in range(shape[0])]
        for i in range(shape[0]):
            for j in range(shape[1]):
                if i < n and j < m:
                    matrix_[i][j] = matrix[i][j]
                else:
                    matrix_[i][j] = 0

        return matrix_