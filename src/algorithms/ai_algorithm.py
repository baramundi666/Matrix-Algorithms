from src.base_algorithm import BaseAlgorithm
import copy
import numpy as np
import math


class Matrix:
    def __init__(self, data, calc, multiplication):
        self.data = copy.deepcopy(data)
        self.calc = calc
        self.multiplication = multiplication
        self.shape = (len(data), len(data[0]))

    def __getitem__(self, idx):
        i, j = idx
        i -= 1
        j -= 1
        return self.data[i][j]

    def __setitem__(self, idx, item):
        i, j = idx
        i -= 1
        j -= 1
        self.data[i][j] = item

    def __neg__(self):
        return Matrix(self.calc.negate(self.data), self.calc, multiplication=self.multiplication)

    def __add__(self, other):
        return Matrix(self.calc.add(self.data, other.data), self.calc, multiplication=self.multiplication)

    def __sub__(self, other):
        return Matrix(self.calc.subtract(self.data, other.data), self.calc, multiplication=self.multiplication)

    def __matmul__(self, other):
        assert self.shape[1] == other.shape[0], "Wrong shape for multiplication"
        return self.multiplication(self, other)

    def __mul__(self, other):
        return self.__matmul__(other)

    @classmethod
    def empty(cls, n: int, m: int, calc, multiplication):
        data = [[None for _ in range(m)] for _ in range(n)]
        return cls(data, calc, multiplication=multiplication)

    @classmethod
    def in_place(cls, data, calc, multiplication):
        retval = Matrix([[]], calc, multiplication=multiplication)
        retval.data = data
        retval.shape = (len(data), len(data[0]))
        return retval




class AIAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()

    @staticmethod
    def ai_compute_h(a, b):
        h = [None] * 77
        h[1] = (a[3, 2]) * (-b[2, 1] - b[2, 5] - b[3, 1])
        h[2] = (a[2, 2] + a[2, 5] - a[3, 5]) * (-b[2, 5] - b[5, 1])
        h[3] = (-a[3, 1] - a[4, 1] + a[4, 2]) * (-b[1, 1] + b[2, 5])
        h[4] = (a[1, 2] + a[1, 4] + a[3, 4]) * (-b[2, 5] - b[4, 1])
        h[5] = (a[1, 5] + a[2, 2] + a[2, 5]) * (-b[2, 4] + b[5, 1])
        h[6] = (-a[2, 2] - a[2, 5] - a[4, 5]) * (b[2, 3] + b[5, 1])
        h[7] = (-a[1, 1] + a[4, 1] - a[4, 2]) * (b[1, 1] + b[2, 4])
        h[8] = (a[3, 2] - a[3, 3] - a[4, 3]) * (-b[2, 3] + b[3, 1])
        h[9] = (-a[1, 2] - a[1, 4] + a[4, 4]) * (b[2, 3] + b[4, 1])
        h[10] = (a[2, 2] + a[2, 5]) * (b[5, 1])
        h[11] = (-a[2, 1] - a[4, 1] + a[4, 2]) * (-b[1, 1] + b[2, 2])
        h[12] = (a[4, 1] - a[4, 2]) * (b[1, 1])
        h[13] = (a[1, 2] + a[1, 4] + a[2, 4]) * (b[2, 2] + b[4, 1])
        h[14] = (a[1, 3] - a[3, 2] + a[3, 3]) * (b[2, 4] + b[3, 1])
        h[15] = (-a[1, 2] - a[1, 4]) * (b[4, 1])
        h[16] = (-a[3, 2] + a[3, 3]) * (b[3, 1])
        h[17] = (a[1, 2] + a[1, 4] - a[2, 1] + a[2, 2] - a[2, 3] + a[2, 4] - a[3, 2] + a[3, 3] - a[4, 1] + a[4, 2]) * (
            b[2, 2])
        h[18] = (a[2, 1]) * (b[1, 1] + b[1, 2] + b[5, 2])
        h[19] = (-a[2, 3]) * (b[3, 1] + b[3, 2] + b[5, 2])
        h[20] = (-a[1, 5] + a[2, 1] + a[2, 3] - a[2, 5]) * (-b[1, 1] - b[1, 2] + b[1, 4] - b[5, 2])
        h[21] = (a[2, 1] + a[2, 3] - a[2, 5]) * (b[5, 2])
        h[22] = (a[1, 3] - a[1, 4] - a[2, 4]) * (b[1, 1] + b[1, 2] - b[1, 4] - b[3, 1] - b[3, 2] + b[3, 4] + b[4, 4])
        h[23] = (a[1, 3]) * (-b[3, 1] + b[3, 4] + b[4, 4])
        h[24] = (a[1, 5]) * (-b[4, 4] - b[5, 1] + b[5, 4])
        h[25] = (-a[1, 1]) * (b[1, 1] - b[1, 4])
        h[26] = (-a[1, 3] + a[1, 4] + a[1, 5]) * (b[4, 4])
        h[27] = (a[1, 3] - a[3, 1] + a[3, 3]) * (b[1, 1] - b[1, 4] + b[1, 5] + b[3, 5])
        h[28] = (-a[3, 4]) * (-b[3, 5] - b[4, 1] - b[4, 5])
        h[29] = (a[3, 1]) * (b[1, 1] + b[1, 5] + b[3, 5])
        h[30] = (a[3, 1] - a[3, 3] + a[3, 4]) * (b[3, 5])
        h[31] = (-a[1, 4] - a[1, 5] - a[3, 4]) * (-b[4, 4] - b[5, 1] + b[5, 4] - b[5, 5])
        h[32] = (a[2, 1] + a[4, 1] + a[4, 4]) * (b[1, 3] - b[4, 1] - b[4, 2] - b[4, 3])
        h[33] = (a[4, 3]) * (-b[3, 1] - b[3, 3])
        h[34] = (a[4, 4]) * (-b[1, 3] + b[4, 1] + b[4, 3])
        h[35] = (-a[4, 5]) * (b[1, 3] + b[5, 1] + b[5, 3])
        h[36] = (a[2, 3] - a[2, 5] - a[4, 5]) * (b[3, 1] + b[3, 2] + b[3, 3] + b[5, 2])
        h[37] = (-a[4, 1] - a[4, 4] + a[4, 5]) * (b[1, 3])
        h[38] = (-a[2, 3] - a[3, 1] + a[3, 3] - a[3, 4]) * (b[3, 5] + b[4, 1] + b[4, 2] + b[4, 5])
        h[39] = (-a[3, 1] - a[4, 1] - a[4, 4] + a[4, 5]) * (b[1, 3] + b[5, 1] + b[5, 3] + b[5, 5])
        h[40] = (-a[1, 3] + a[1, 4] + a[1, 5] - a[4, 4]) * (-b[3, 1] - b[3, 3] + b[3, 4] + b[4, 4])
        h[41] = (-a[1, 1] + a[4, 1] - a[4, 5]) * (b[1, 3] + b[3, 1] + b[3, 3] - b[3, 4] + b[5, 1] + b[5, 3] - b[5, 4])
        h[42] = (-a[2, 1] + a[2, 5] - a[3, 5]) * (-b[1, 1] - b[1, 2] - b[1, 5] + b[4, 1] + b[4, 2] + b[4, 5] - b[5, 2])
        h[43] = (a[2, 4]) * (b[4, 1] + b[4, 2])
        h[44] = (a[2, 3] + a[3, 2] - a[3, 3]) * (b[2, 2] - b[3, 1])
        h[45] = (-a[3, 3] + a[3, 4] - a[4, 3]) * (b[3, 5] + b[4, 1] + b[4, 3] + b[4, 5] + b[5, 1] + b[5, 3] + b[5, 5])
        h[46] = (-a[3, 5]) * (-b[5, 1] - b[5, 5])
        h[47] = (a[2, 1] - a[2, 5] - a[3, 1] + a[3, 5]) * (b[1, 1] + b[1, 2] + b[1, 5] - b[4, 1] - b[4, 2] - b[4, 5])
        h[48] = (-a[2, 3] + a[3, 3]) * (b[2, 2] + b[3, 2] + b[3, 5] + b[4, 1] + b[4, 2] + b[4, 5])
        h[49] = (-a[1, 1] - a[1, 3] + a[1, 4] + a[1, 5] - a[2, 1] - a[2, 3] + a[2, 4] + a[2, 5]) * (
                -b[1, 1] - b[1, 2] + b[1, 4])
        h[50] = (-a[1, 4] - a[2, 4]) * (b[2, 2] - b[3, 1] - b[3, 2] + b[3, 4] - b[4, 2] + b[4, 4])
        h[51] = (a[2, 2]) * (b[2, 1] + b[2, 2] - b[5, 1])
        h[52] = (a[4, 2]) * (b[1, 1] + b[2, 1] + b[2, 3])
        h[53] = (-a[1, 2]) * (-b[2, 1] + b[2, 4] + b[4, 1])
        h[54] = (a[1, 2] + a[1, 4] - a[2, 2] - a[2, 5] - a[3, 2] + a[3, 3] - a[4, 2] + a[4, 3] - a[4, 4] - a[4, 5]) * (
            b[2, 3])
        h[55] = (a[1, 4] - a[4, 4]) * (-b[2, 3] + b[3, 1] + b[3, 3] - b[3, 4] + b[4, 3] - b[4, 4])
        h[56] = (a[1, 1] - a[1, 5] - a[4, 1] + a[4, 5]) * (b[3, 1] + b[3, 3] - b[3, 4] + b[5, 1] + b[5, 3] - b[5, 4])
        h[57] = (-a[3, 1] - a[4, 1]) * (-b[1, 3] - b[1, 5] - b[2, 5] - b[5, 1] - b[5, 3] - b[5, 5])
        h[58] = (-a[1, 4] - a[1, 5] - a[3, 4] - a[3, 5]) * (-b[5, 1] + b[5, 4] - b[5, 5])
        h[59] = (-a[3, 3] + a[3, 4] - a[4, 3] + a[4, 4]) * (b[4, 1] + b[4, 3] + b[4, 5] + b[5, 1] + b[5, 3] + b[5, 5])
        h[60] = (a[2, 5] + a[4, 5]) * (b[2, 3] - b[3, 1] - b[3, 2] - b[3, 3] - b[5, 2] - b[5, 3])
        h[61] = (a[1, 4] + a[3, 4]) * (
                b[1, 1] - b[1, 4] + b[1, 5] - b[2, 5] - b[4, 4] + b[4, 5] - b[5, 1] + b[5, 4] - b[5, 5])
        h[62] = (a[2, 1] + a[4, 1]) * (b[1, 2] + b[1, 3] + b[2, 2] - b[4, 1] - b[4, 2] - b[4, 3])
        h[63] = (-a[3, 3] - a[4, 3]) * (-b[2, 3] - b[3, 3] - b[3, 5] - b[4, 1] - b[4, 3] - b[4, 5])
        h[64] = (a[1, 1] - a[1, 3] - a[1, 4] + a[3, 1] - a[3, 3] - a[3, 4]) * (b[1, 1] - b[1, 4] + b[1, 5])
        h[65] = (-a[1, 1] + a[4, 1]) * (-b[1, 3] + b[1, 4] + b[2, 4] - b[5, 1] - b[5, 3] + b[5, 4])
        h[66] = (a[1, 1] - a[1, 2] + a[1, 3] - a[1, 5] - a[2, 2] - a[2, 5] - a[3, 2] + a[3, 3] - a[4, 1] + a[4, 2]) * (
            b[2, 4])
        h[67] = (a[2, 5] - a[3, 5]) * (
                b[1, 1] + b[1, 2] + b[1, 5] - b[2, 5] - b[4, 1] - b[4, 2] - b[4, 5] + b[5, 2] + b[5, 5])
        h[68] = (a[1, 1] + a[1, 3] - a[1, 4] - a[1, 5] - a[4, 1] - a[4, 3] + a[4, 4] + a[4, 5]) * (
                -b[3, 1] - b[3, 3] + b[3, 4])
        h[69] = (-a[1, 3] + a[1, 4] - a[2, 3] + a[2, 4]) * (-b[2, 4] - b[3, 1] - b[3, 2] + b[3, 4] - b[5, 2] + b[5, 4])
        h[70] = (a[2, 3] - a[2, 5] + a[4, 3] - a[4, 5]) * (-b[3, 1] - b[3, 2] - b[3, 3])
        h[71] = (-a[3, 1] + a[3, 3] - a[3, 4] + a[3, 5] - a[4, 1] + a[4, 3] - a[4, 4] + a[4, 5]) * (
                -b[5, 1] - b[5, 3] - b[5, 5])
        h[72] = (-a[2, 1] - a[2, 4] - a[4, 1] - a[4, 4]) * (b[4, 1] + b[4, 2] + b[4, 3])
        h[73] = (a[1, 3] - a[1, 4] - a[1, 5] + a[2, 3] - a[2, 4] - a[2, 5]) * (
                b[1, 1] + b[1, 2] - b[1, 4] + b[2, 4] + b[5, 2] - b[5, 4])
        h[74] = (a[2, 1] - a[2, 3] + a[2, 4] - a[3, 1] + a[3, 3] - a[3, 4]) * (b[4, 1] + b[4, 2] + b[4, 5])
        h[75] = -(a[1, 2] + a[1, 4] - a[2, 2] - a[2, 5] - a[3, 1] + a[3, 2] + a[3, 4] + a[3, 5] - a[4, 1] + a[4, 2]) * (
            b[2, 5])
        h[76] = (a[1, 3] + a[3, 3]) * (-b[1, 1] + b[1, 4] - b[1, 5] + b[2, 4] + b[3, 4] - b[3, 5])

        return h

    def ai_compute_c(self, h, multiplication):
        c = Matrix.empty(4, 5, self.calc, multiplication=multiplication)

        c[1, 1] = -h[10] + h[12] + h[14] - h[15] - h[16] + h[53] + h[5] - h[66] - h[7]
        c[2, 1] = h[10] + h[11] - h[12] + h[13] + h[15] + h[16] - h[17] - h[44] + h[51]
        c[3, 1] = h[10] - h[12] + h[15] + h[16] - h[1] + h[2] + h[3] - h[4] + h[75]
        c[4, 1] = -h[10] + h[12] - h[15] - h[16] + h[52] + h[54] - h[6] - h[8] + h[9]
        c[1, 2] = h[13] + h[15] + h[20] + h[21] - h[22] + h[23] + h[25] - h[43] + h[49] + h[50]
        c[2, 2] = -h[11] + h[12] - h[13] - h[15] - h[16] + h[17] + h[18] - h[19] - h[21] + h[43] + h[44]
        c[3, 2] = -h[16] - h[19] - h[21] - h[28] - h[29] - h[38] + h[42] + h[44] - h[47] + h[48]
        c[4, 2] = h[11] - h[12] - h[18] + h[21] - h[32] + h[33] - h[34] - h[36] + h[62] - h[70]
        c[1, 3] = h[15] + h[23] + h[24] + h[34] - h[37] + h[40] - h[41] + h[55] - h[56] - h[9]
        c[2, 3] = -h[10] + h[19] + h[32] + h[35] + h[36] + h[37] - h[43] - h[60] - h[6] - h[72]
        c[3, 3] = -h[16] - h[28] + h[33] + h[37] - h[39] + h[45] - h[46] + h[63] - h[71] - h[8]
        c[4, 3] = h[10] + h[15] + h[16] - h[33] + h[34] - h[35] - h[37] - h[54] + h[6] + h[8] - h[9]
        c[1, 4] = -h[10] + h[12] + h[14] - h[16] + h[23] + h[24] + h[25] + h[26] + h[5] - h[66] - h[7]
        c[2, 4] = h[10] + h[18] - h[19] + h[20] - h[22] - h[24] - h[26] - h[5] - h[69] + h[73]
        c[3, 4] = -h[14] + h[16] - h[23] - h[26] + h[27] + h[29] + h[31] + h[46] - h[58] + h[76]
        c[4, 4] = h[12] + h[25] + h[26] - h[33] - h[35] - h[40] + h[41] + h[65] - h[68] - h[7]
        c[1, 5] = h[15] + h[24] + h[25] + h[27] - h[28] + h[30] + h[31] - h[4] + h[61] + h[64]
        c[2, 5] = -h[10] - h[18] - h[2] - h[30] - h[38] + h[42] - h[43] + h[46] + h[67] + h[74]
        c[3, 5] = -h[10] + h[12] - h[15] + h[28] + h[29] - h[2] - h[30] - h[3] + h[46] + h[4] - h[75]
        c[4, 5] = -h[12] - h[29] + h[30] - h[34] + h[35] + h[39] + h[3] - h[45] + h[57] + h[59]

        return c

    def ai_multiplication(self, a, b):
        h = self.ai_compute_h(a, b)
        return self.ai_compute_c(h, multiplication=a.multiplication)

    @staticmethod
    def submatrix(a, yrange: tuple[int, int], xrange: tuple[int, int]):
        data = [[a[i, j] for j in range(*xrange)] for i in range(*yrange)]
        return Matrix.in_place(data, a.calc, a.multiplication)

    @staticmethod
    def _plant(dest, src, offset: tuple[int, int], src_shape: tuple[int, int]):
        for i in range(src_shape[0]):
            for j in range(src_shape[1]):
                dest[i + offset[0]][j + offset[1]] = src[i][j]

    @staticmethod
    def expand(a):
        cy = [0] + list(np.cumsum([a[i, 1].shape[0] for i in range(1, a.shape[0] + 1)]))
        cx = [0] + list(np.cumsum([a[1, i].shape[1] for i in range(1, a.shape[1] + 1)]))
        N = cy[-1]
        M = cx[-1]
        data = [[None] * M for _ in range(N)]

        n, m = a.shape
        for i in range(n):
            for j in range(m):
                offset = (cy[i], cx[j])
                src = a[i + 1, j + 1]
                AIAlgorithm._plant(data, src.data, offset, src.shape)

        return Matrix.in_place(data, a.calc, a.multiplication)
    def block(self, a, shape: tuple[int, int]):
        assert a.shape[0] >= shape[0] and a.shape[1] >= shape[1], "Matrix too small"

        n, m = a.shape
        y = n // shape[0]
        x = m // shape[1]

        retval = Matrix.empty(*shape, self.calc, multiplication=a.multiplication)
        for i in range(1, shape[0] + 1):
            for j in range(1, shape[1] + 1):
                yrange = ((i - 1) * y + 1, i * y + 1)
                xrange = ((j - 1) * x + 1, j * x + 1)
                if i == shape[0]:
                    yrange = (yrange[0], n + 1)
                if j == shape[1]:
                    xrange = (xrange[0], m + 1)
                retval[i, j] = self.submatrix(a, yrange, xrange)

        return retval

    def __ai(self, A, B):
        a = Matrix(A, self.calc, multiplication=self.recursive_ai)
        b = Matrix(B, self.calc, multiplication=self.recursive_ai)
        return (a @ b).data

    @staticmethod
    def power(a: int, b: int) -> int:
        return b ** math.ceil(math.log(a, b))

    def rescale(self, a, shape):
        data = [[0] * shape[1] for _ in range(shape[0])]

        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                data[i][j] = a[i + 1, j + 1]

        return Matrix.in_place(data, self.calc, multiplication=a.multiplication)
    def recursive_ai(self, a, b):
        # Scales up matrices to powers of 4 and 5 by appending zeroes
        if a.shape[0] < 4 or a.shape[1] < 5 or b.shape[0] < 5 or b.shape[1] < 5:
            return Matrix(self.calc.standard_matrix_multiplication(a.data, b.data), self.calc, multiplication=a.multiplication)
        n, k = a.shape
        k, m = b.shape
        a = self.rescale(a, shape=(self.power(n, 4), self.power(k, 5)))
        b = self.rescale(b, shape=(self.power(k, 5), self.power(m, 5)))
        a.multiplication = self.recursive_ai_rec
        b.multiplication = self.recursive_ai_rec
        retval = self.recursive_ai_rec(a, b)

        return self.submatrix(retval, yrange=(1, n + 1), xrange=(1, m + 1))

    def recursive_ai_rec(self, a, b):
        # Works only for powers of 4 and 5
        if a.shape[0] < 4 or a.shape[1] < 5 or b.shape[0] < 5 or b.shape[1] < 5:
            return Matrix(self.calc.standard_matrix_multiplication(a.data, b.data), self.calc, multiplication=a.multiplication)

        A = self.block(a, shape=(4, 5))
        B = self.block(b, shape=(5, 5))
        return self.expand(self.ai_multiplication(A, B))

    def run(self, A, B):
        self.matrix_3 = self.__ai(A, B)

    def __local_test(self):
        A1 = [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10],
            [11, 12, 13, 14, 15],
            [16, 17, 18, 19, 20]
        ]

        B1 = [
            [1, 1, 1, 0, 1],
            [0, 1, 0, 1, 0],
            [1, 0, 1, 1, 1],
            [0, 1, 1, 0, 0],
            [1, 0, 1, 1, 1]
        ]
        self.run(A1, B1)
        result = self.matrix_3
        result2 = self.calc.standard_matrix_multiplication(A1, B1)
        print(result)
        print(result2)
        assert result2 == result, "Error"


