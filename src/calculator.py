class Calculator:
    def __init__(self):
        self.add_count = 0
        self.subtract_count = 0
        self.negate_count = 0
        self.multiply_count = 0

    def reset_counters(self):
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
                self.negate_count += 1
                matrix_[i][j] = -matrix[i][j]
        return matrix_

    def multiply_one_by_one_matrices(self, matrix_1, matrix_2):
        # atomic multiplication
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