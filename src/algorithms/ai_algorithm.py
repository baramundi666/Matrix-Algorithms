class AIALGORITHM:
    def __init__(self):
        self.h = [0 for _ in range(76)]

    # Dodawanie dwóch macierzy
    def add_matrices(self, A, B):
        return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    # Odejmowanie dwóch macierzy
    def subtract_matrices(self, A, B):
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    # Mnożenie dwóch macierzy
    def multiply_matrices(self, A, B):
        result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    # Negacja elementów macierzy
    def negate_matrix(self, M):
        return [[-M[i][j] for j in range(len(M[0]))] for i in range(len(M))]

    # Dzielenie macierzy na bloki
    def divide_matrix(self, M, num_block_rows, num_block_cols):
        rows = len(M)
        cols = len(M[0])
        block_height = rows // num_block_rows
        block_width = cols // num_block_cols

        blocks = []

        for i in range(num_block_rows):
            row_blocks = []
            for j in range(num_block_cols):
                block = []
                for row in range(block_height * i, block_height * (i + 1)):
                    block_row = []
                    for col in range(block_width * j, block_width * (j + 1)):
                        block_row.append(M[row][col])
                    block.append(block_row)
                row_blocks.append(block)
            blocks.append(row_blocks)
        return blocks

    # Wypełnianie macierzy wynikowej
    def fill_matrix(self, C, m, k, height, width):
        C_result = [[0] * k for _ in range(m)]
        for i in range(4):
            for j in range(5):
                block = C[i][j]
                for x in range(height):
                    for y in range(width):
                        C_result[i * height + x][j * width + y] = block

        return C_result

    # Metoda wykonująca algorytm ai
    def ai(self, A, B):
        m = len(A)
        n = len(A[0])
        k = len(B[0])
        if m % 4 != 0 or n % 5 != 0 or k % 5 != 0:
            return self.multiply_matrices(A, B)

        C = [[0] * 5 for _ in range(4)]

        A_blocks = self.divide_matrix(A, 4, 5)
        B_blocks = self.divide_matrix(B, 5, 5)

        self.h[0] = self.ai(A_blocks[2][1], self.subtract_matrices(
            self.subtract_matrices(self.negate_matrix(B_blocks[1][0]), B_blocks[1][4]), B_blocks[2][0]))

        self.h[1] = self.ai(self.add_matrices(A_blocks[1][1], self.subtract_matrices(A_blocks[1][4], A_blocks[2][4])),
                            self.negate_matrix(self.add_matrices(B_blocks[1][4], B_blocks[4][0])))

        self.h[2] = self.ai(
            self.add_matrices(self.subtract_matrices(self.negate_matrix(A_blocks[2][0]), A_blocks[3][0]),
                                   A_blocks[3][1]), self.add_matrices(self.negate_matrix(B_blocks[0][0]), B_blocks[1][4]))

        self.h[3] = self.ai(self.add_matrices(self.add_matrices(A_blocks[0][1], A_blocks[0][3]), A_blocks[2][3]),
                            self.negate_matrix(self.add_matrices(B_blocks[1][4], B_blocks[3][0])))

        self.h[4] = self.ai(self.add_matrices(self.add_matrices(A_blocks[0][4], A_blocks[1][1]), A_blocks[1][4]),
                            self.add_matrices(self.negate_matrix(B_blocks[1][3]), B_blocks[4][0]))

        self.h[5] = self.ai(
            self.subtract_matrices(self.subtract_matrices(self.negate_matrix(A_blocks[1][1]), A_blocks[1][4]),
                                   A_blocks[3][4]), self.add_matrices(B_blocks[1][2], B_blocks[4][0]))

        self.h[6] = self.ai(
            self.subtract_matrices(self.add_matrices(self.negate_matrix(A_blocks[0][0]), A_blocks[3][0]),
                                   A_blocks[3][1]), self.add_matrices(B_blocks[0][0], B_blocks[1][3]))

        self.h[7] = self.ai(self.subtract_matrices(A_blocks[2][1], self.add_matrices(A_blocks[2][2], A_blocks[3][2])),
                            self.add_matrices(self.negate_matrix(B_blocks[1][2]), B_blocks[2][0]))

        self.h[8] = self.ai(
            self.add_matrices(self.subtract_matrices(self.negate_matrix(A_blocks[0][1]), A_blocks[0][3]),
                              A_blocks[3][3]), self.add_matrices(B_blocks[1][2], B_blocks[3][0]))

        self.h[9] = self.ai(self.add_matrices(A_blocks[1][1], A_blocks[1][4]), B_blocks[4][0])

        self.h[10] = self.ai(
            self.add_matrices(self.subtract_matrices(self.negate_matrix(A_blocks[1][0]), A_blocks[3][0]),
                              A_blocks[3][1]), self.add_matrices(self.negate_matrix(B_blocks[0][0]), B_blocks[1][1]))

        self.h[11] = self.ai(self.subtract_matrices(A_blocks[3][0], A_blocks[3][1]), B_blocks[0][0])
        self.h[12] = self.ai(self.add_matrices(self.add_matrices(A_blocks[0][1], A_blocks[0][3]), A_blocks[1][3]),
                             self.add_matrices(B_blocks[1][1], B_blocks[3][0]))
        self.h[13] = self.ai(self.add_matrices(self.subtract_matrices(A_blocks[0][2], A_blocks[2][1]), A_blocks[2][2]),
                             self.add_matrices(B_blocks[1][3], B_blocks[2][0]))
        self.h[14] = self.ai(self.subtract_matrices(self.negate_matrix(A_blocks[0][1]), A_blocks[0][3]), B_blocks[3][0])
        self.h[15] = self.ai(self.add_matrices(self.negate_matrix(A_blocks[2][1]), A_blocks[2][2]), B_blocks[2][0])
        self.h[16] = self.ai(
            self.add_matrices(
                self.subtract_matrices(
                    self.add_matrices(
                        self.subtract_matrices(
                            self.add_matrices(
                                self.subtract_matrices(
                                    self.add_matrices(
                                        self.subtract_matrices(
                                            self.add_matrices(A_blocks[0][1], A_blocks[0][3]),
                                            A_blocks[1][0]
                                        ),
                                        A_blocks[1][1]
                                    ),
                                    A_blocks[1][2]
                                ),
                                A_blocks[1][3]
                            ),
                            A_blocks[2][1]
                        ),
                        A_blocks[2][2]
                    ),
                    A_blocks[3][0]
                ),
                A_blocks[3][1]
            ),
            B_blocks[1][1]
        )
        self.h[17] = self.ai(A_blocks[1][0],
                             self.add_matrices(self.add_matrices(B_blocks[0][0], B_blocks[0][1]), B_blocks[4][1]))
        self.h[18] = self.ai(self.negate_matrix(A_blocks[1][2]),
                             self.add_matrices(self.add_matrices(B_blocks[2][0], B_blocks[2][1]), B_blocks[4][1]))
        self.h[19] = self.ai(self.add_matrices(
            self.add_matrices(self.add_matrices(self.negate_matrix(A_blocks[0][4]), A_blocks[1][0]), A_blocks[1][2]),
            self.negate_matrix(A_blocks[1][4])), self.subtract_matrices(
            self.add_matrices(self.subtract_matrices(self.negate_matrix(B_blocks[0][0]), B_blocks[0][1]),
                              B_blocks[0][3]), B_blocks[4][1]))
        self.h[20] = self.ai(
            self.add_matrices(self.add_matrices(A_blocks[1][0], A_blocks[1][2]), self.negate_matrix(A_blocks[1][4])),
            B_blocks[4][1])
        self.h[21] = self.ai(
            self.subtract_matrices(self.subtract_matrices(A_blocks[0][2], A_blocks[0][3]), A_blocks[1][3]),
            self.add_matrices(
                self.add_matrices(
                    self.subtract_matrices(
                        self.add_matrices(
                            self.add_matrices(self.add_matrices(B_blocks[0][0], B_blocks[0][1]),
                                              self.negate_matrix(B_blocks[0][3])),
                            self.negate_matrix(B_blocks[2][0])
                        ),
                        B_blocks[2][1]
                    ),
                    B_blocks[2][3]
                ),
                B_blocks[3][3]
            )
        )

        self.h[22] = self.ai(A_blocks[0][2],
                             self.add_matrices(self.add_matrices(self.negate_matrix(B_blocks[2][0]), B_blocks[2][3]),
                                               B_blocks[3][3]))

        self.h[23] = self.ai(A_blocks[0][4],
                             self.add_matrices(
                                 self.subtract_matrices(self.negate_matrix(B_blocks[3][3]), B_blocks[4][0]),
                                 B_blocks[4][3]))

        self.h[24] = self.ai(self.negate_matrix(A_blocks[0][0]),
                             self.subtract_matrices(B_blocks[0][0], B_blocks[0][3]))

        self.h[25] = self.ai(
            self.add_matrices(self.add_matrices(self.negate_matrix(A_blocks[0][2]), A_blocks[0][3]), A_blocks[0][4]),
            B_blocks[3][3])

        self.h[26] = self.ai(self.add_matrices(self.subtract_matrices(A_blocks[0][2], A_blocks[2][0]), A_blocks[2][2]),
                             self.add_matrices(self.add_matrices(self.subtract_matrices(B_blocks[0][0], B_blocks[0][3]),
                                                                 B_blocks[0][4]), B_blocks[2][4]))

        self.h[27] = self.ai(self.negate_matrix(A_blocks[2][3]),
                             self.negate_matrix(
                                 self.add_matrices(self.add_matrices(B_blocks[2][4], B_blocks[3][0]), B_blocks[3][4])))

        self.h[28] = self.ai(A_blocks[2][0],
                             self.add_matrices(self.add_matrices(B_blocks[0][0], B_blocks[0][4]), B_blocks[2][4]))

        self.h[29] = self.ai(self.add_matrices(self.subtract_matrices(A_blocks[2][0], A_blocks[2][2]), A_blocks[2][3]),
                             B_blocks[2][4])

        self.h[30] = self.ai(
            self.subtract_matrices(
                self.subtract_matrices(self.negate_matrix(A_blocks[0][3]), A_blocks[0][4]),
                A_blocks[2][3]
            ),
            self.subtract_matrices(
                self.add_matrices(
                    self.subtract_matrices(self.negate_matrix(B_blocks[3][3]), B_blocks[4][0]),
                    B_blocks[4][3]
                ),
                B_blocks[4][4]
            )
        )

        self.h[31] = self.ai(self.add_matrices(self.add_matrices(A_blocks[1][0], A_blocks[3][0]), A_blocks[3][3]),
                             self.subtract_matrices(
                                 self.subtract_matrices(self.subtract_matrices(B_blocks[0][2], B_blocks[3][0]),
                                                        B_blocks[3][1]), B_blocks[3][2]))

        self.h[32] = self.ai(A_blocks[3][2],
                             self.negate_matrix(self.add_matrices(B_blocks[2][0], B_blocks[2][2])))

        self.h[33] = self.ai(A_blocks[3][3],
                             self.add_matrices(self.add_matrices(self.negate_matrix(B_blocks[0][2]), B_blocks[3][0]),
                                               B_blocks[3][2]))

        self.h[34] = self.ai(self.negate_matrix(A_blocks[3][4]),
                             self.add_matrices(self.add_matrices(B_blocks[0][2], B_blocks[4][0]), B_blocks[4][2]))

        self.h[35] = self.ai(
            self.subtract_matrices(self.subtract_matrices(A_blocks[1][2], A_blocks[1][4]), A_blocks[3][4]),
            self.add_matrices(self.add_matrices(self.add_matrices(B_blocks[2][0], B_blocks[2][1]), B_blocks[2][2]),
                              B_blocks[4][1]))

        self.h[36] = self.ai(
            self.add_matrices(self.subtract_matrices(self.negate_matrix(A_blocks[3][0]), A_blocks[3][3]),
                              A_blocks[3][4]),
            B_blocks[0][2])

        self.h[37] = self.ai(self.subtract_matrices(
            self.add_matrices(self.subtract_matrices(self.negate_matrix(A_blocks[1][2]), A_blocks[2][0]),
                              A_blocks[2][2]), A_blocks[2][3]),
                             self.add_matrices(
                                 self.add_matrices(self.add_matrices(B_blocks[2][4], B_blocks[3][0]), B_blocks[3][1]),
                                 B_blocks[3][4]))

        self.h[38] = self.ai(self.add_matrices(
            self.subtract_matrices(self.subtract_matrices(self.negate_matrix(A_blocks[2][0]), A_blocks[3][0]),
                                   A_blocks[3][3]), A_blocks[3][4]),
                             self.add_matrices(
                                 self.add_matrices(self.add_matrices(B_blocks[0][2], B_blocks[4][0]), B_blocks[4][2]),
                                 B_blocks[4][4]))

        self.h[39] = self.ai(self.add_matrices(
            self.add_matrices(self.add_matrices(self.negate_matrix(A_blocks[0][2]), A_blocks[0][3]), A_blocks[0][4]),
            self.negate_matrix(A_blocks[3][3])),
                             self.add_matrices(self.add_matrices(
                                 self.subtract_matrices(self.negate_matrix(B_blocks[2][0]), B_blocks[2][2]),
                                 B_blocks[2][3]), B_blocks[3][3]))

        self.h[40] = self.ai(
            self.subtract_matrices(self.add_matrices(self.negate_matrix(A_blocks[0][0]), A_blocks[3][0]),
                                   A_blocks[3][4]),
            self.subtract_matrices(self.add_matrices(self.add_matrices(self.subtract_matrices(
                self.add_matrices(self.add_matrices(B_blocks[0][2], B_blocks[2][0]), B_blocks[2][2]), B_blocks[2][3]),
                                                                       B_blocks[4][0]), B_blocks[4][2]),
                                   B_blocks[4][3]))

        self.h[41] = self.ai(
            self.subtract_matrices(self.add_matrices(self.negate_matrix(A_blocks[1][0]), A_blocks[1][4]),
                                   A_blocks[2][4]),
            self.subtract_matrices(self.add_matrices(self.add_matrices(self.add_matrices(
                self.add_matrices(self.subtract_matrices(self.negate_matrix(B_blocks[0][0]), B_blocks[0][1]),
                                  self.negate_matrix(B_blocks[0][4])),
                B_blocks[3][0]), B_blocks[3][1]), B_blocks[3][4]), B_blocks[4][1]))

        self.h[42] = self.ai(A_blocks[1][3],
                             self.add_matrices(B_blocks[3][0], B_blocks[3][1]))

        self.h[43] = self.ai(
            self.add_matrices(self.add_matrices(A_blocks[1][2], A_blocks[2][1]), self.negate_matrix(A_blocks[2][2])),
            self.subtract_matrices(B_blocks[1][1], B_blocks[2][0]))

        self.h[44] = self.ai(
            self.add_matrices(
                self.add_matrices(self.negate_matrix(A_blocks[2][2]), A_blocks[2][3]),
                self.negate_matrix(A_blocks[3][2])
            ),
            self.add_matrices(
                self.add_matrices(
                    self.add_matrices(B_blocks[2][4], B_blocks[3][0]),
                    B_blocks[3][2]
                ),
                self.add_matrices(
                    self.add_matrices(B_blocks[3][4], B_blocks[4][0]),
                    self.add_matrices(B_blocks[4][2], B_blocks[4][4])
                )
            )
        )

        self.h[45] = self.ai(self.negate_matrix(A_blocks[2][4]),
                             self.negate_matrix(self.add_matrices(B_blocks[4][0], B_blocks[4][4])))

        self.h[46] = self.ai(self.add_matrices(
            self.subtract_matrices(self.subtract_matrices(A_blocks[1][0], A_blocks[1][4]), A_blocks[2][0]),
            A_blocks[2][4]),
                             self.subtract_matrices(self.subtract_matrices(self.subtract_matrices(
                                 self.add_matrices(self.add_matrices(B_blocks[0][0], B_blocks[0][1]), B_blocks[0][4]),
                                 B_blocks[3][0]), B_blocks[3][1]), B_blocks[3][4]))

        self.h[47] = self.ai(self.add_matrices(self.negate_matrix(A_blocks[1][2]), A_blocks[2][2]),
                             self.add_matrices(self.add_matrices(self.add_matrices(
                                 self.add_matrices(self.add_matrices(B_blocks[1][1], B_blocks[2][1]), B_blocks[2][4]),
                                 B_blocks[3][0]), B_blocks[3][1]), B_blocks[3][4]))

        self.h[48] = self.ai(self.add_matrices(self.add_matrices(self.subtract_matrices(self.subtract_matrices(
            self.add_matrices(
                self.add_matrices(self.subtract_matrices(self.negate_matrix(A_blocks[0][0]), A_blocks[0][2]),
                                  A_blocks[0][3]),
                A_blocks[0][4]), A_blocks[1][0]), A_blocks[1][2]), A_blocks[1][3]), A_blocks[1][4]),
                             self.add_matrices(
                                 self.subtract_matrices(self.negate_matrix(B_blocks[0][0]), B_blocks[0][1]),
                                 B_blocks[0][3]))

        self.h[49] = self.ai(self.subtract_matrices(self.negate_matrix(A_blocks[0][3]), A_blocks[1][3]),
                             self.add_matrices(self.subtract_matrices(self.add_matrices(
                                 self.subtract_matrices(self.subtract_matrices(B_blocks[1][1], B_blocks[2][0]),
                                                        B_blocks[2][1]),
                                 B_blocks[2][3]), B_blocks[3][1]), B_blocks[3][3]))

        self.h[50] = self.ai(A_blocks[1][1],
                             self.add_matrices(self.add_matrices(B_blocks[1][0], B_blocks[1][1]),
                                               self.negate_matrix(B_blocks[4][0])))

        self.h[51] = self.ai(A_blocks[3][1],
                             self.add_matrices(self.add_matrices(B_blocks[0][0], B_blocks[1][0]), B_blocks[1][2]))

        self.h[52] = self.ai(
            self.negate_matrix(A_blocks[0][1]),
            self.add_matrices(
                self.add_matrices(self.negate_matrix(B_blocks[1][0]), B_blocks[1][3]),
                B_blocks[3][0]
            )
        )

        self.h[53] = self.ai(self.subtract_matrices(self.subtract_matrices(self.add_matrices(self.subtract_matrices(
            self.add_matrices(self.subtract_matrices(self.subtract_matrices(
                self.subtract_matrices(self.add_matrices(A_blocks[0][1], A_blocks[0][3]), A_blocks[1][1]),
                A_blocks[1][4]),
                                                     A_blocks[2][1]), A_blocks[2][2]), A_blocks[3][1]), A_blocks[3][2]),
                                                                           A_blocks[3][3]), A_blocks[3][4]),
                             B_blocks[1][2])

        self.h[54] = self.ai(
            self.subtract_matrices(A_blocks[0][3], A_blocks[3][3]),
            self.subtract_matrices(self.add_matrices(
                self.subtract_matrices(
                    self.add_matrices(
                        self.add_matrices(self.negate_matrix(B_blocks[1][2]), B_blocks[2][0]), B_blocks[2][2]),
                    B_blocks[2][3]), B_blocks[3][2]), B_blocks[3][3]))

        self.h[55] = self.ai(self.add_matrices(
            self.subtract_matrices(self.subtract_matrices(A_blocks[0][0], A_blocks[0][4]), A_blocks[3][0]),
            A_blocks[3][4]),
                             self.add_matrices(self.subtract_matrices(self.add_matrices(B_blocks[2][0], B_blocks[2][2]),
                                                                      B_blocks[2][3]),
                                               self.subtract_matrices(self.add_matrices(B_blocks[4][0], B_blocks[4][2]),
                                                                      B_blocks[4][3])))

        self.h[56] = self.ai(self.subtract_matrices(self.negate_matrix(A_blocks[2][0]), A_blocks[3][0]),
                             self.subtract_matrices(self.subtract_matrices(self.subtract_matrices(
                                 self.subtract_matrices(
                                     self.subtract_matrices(self.negate_matrix(B_blocks[0][2]), B_blocks[0][4]),
                                     B_blocks[1][4]), B_blocks[4][0]), B_blocks[4][2]), B_blocks[4][4]))

        self.h[57] = self.ai(self.subtract_matrices(
            self.subtract_matrices(self.subtract_matrices(self.negate_matrix(A_blocks[0][3]), A_blocks[0][4]),
                                   A_blocks[2][3]), A_blocks[2][4]),
                             self.subtract_matrices(
                                 self.add_matrices(self.negate_matrix(B_blocks[4][0]), B_blocks[4][3]), B_blocks[4][4]))

        self.h[58] = self.ai(self.add_matrices(
            self.subtract_matrices(self.add_matrices(self.negate_matrix(A_blocks[2][2]), A_blocks[2][3]),
                                   A_blocks[3][2]), A_blocks[3][3]),
                             self.add_matrices(self.add_matrices(self.add_matrices(
                                 self.add_matrices(self.add_matrices(B_blocks[3][0], B_blocks[3][2]), B_blocks[3][4]),
                                 B_blocks[4][0]), B_blocks[4][2]), B_blocks[4][4]))

        self.h[59] = self.ai(self.add_matrices(A_blocks[1][4], A_blocks[3][4]),
                             self.subtract_matrices(self.subtract_matrices(self.subtract_matrices(
                                 self.subtract_matrices(self.subtract_matrices(B_blocks[1][2], B_blocks[2][0]),
                                                        B_blocks[2][1]), B_blocks[2][2]), B_blocks[4][1]),
                                                    B_blocks[4][2]))

        self.h[60] = self.ai(
            self.add_matrices(A_blocks[0][3], A_blocks[2][3]),
            self.subtract_matrices(
                self.add_matrices(
                    self.subtract_matrices(
                        self.add_matrices(
                            self.subtract_matrices(
                                self.subtract_matrices(
                                    self.add_matrices(
                                        self.subtract_matrices(B_blocks[0][0], B_blocks[0][3]),
                                        B_blocks[0][4]
                                    ), B_blocks[1][4]),
                                B_blocks[3][3]), B_blocks[3][4]),
                        B_blocks[4][0]), B_blocks[4][3]), B_blocks[4][0])
        )

        self.h[61] = self.ai(self.add_matrices(A_blocks[1][0], A_blocks[3][0]),
                             self.subtract_matrices(self.subtract_matrices(self.subtract_matrices(
                                 self.add_matrices(self.add_matrices(B_blocks[0][1], B_blocks[0][2]), B_blocks[1][1]),
                                 B_blocks[3][0]), B_blocks[3][1]), B_blocks[3][2]))

        self.h[62] = self.ai(
            self.subtract_matrices(self.negate_matrix(A_blocks[2][2]), A_blocks[3][2]),
            self.subtract_matrices(
                self.subtract_matrices(
                    self.subtract_matrices(
                        self.subtract_matrices(
                            self.subtract_matrices(self.negate_matrix(B_blocks[1][2]), B_blocks[2][2]),
                            B_blocks[2][4]), B_blocks[3][0]), B_blocks[3][2]), B_blocks[3][4]))

        self.h[63] = self.ai(
            self.subtract_matrices(
                self.subtract_matrices(
                    self.add_matrices(
                        self.subtract_matrices(
                            self.subtract_matrices(A_blocks[0][0], A_blocks[0][2]),
                            A_blocks[0][3]
                        ), A_blocks[2][0]), A_blocks[2][2]), A_blocks[2][3]

            ),
            self.add_matrices(
                self.subtract_matrices(B_blocks[0][0], B_blocks[0][3]),
                B_blocks[0][4]
            )
        )

        self.h[64] = self.ai(
            self.add_matrices(self.negate_matrix(A_blocks[0][0]), A_blocks[3][0]),
            self.add_matrices(
                self.subtract_matrices(
                    self.subtract_matrices(
                        self.add_matrices(
                            self.add_matrices(self.negate_matrix(B_blocks[0][2]), B_blocks[0][3]),
                            B_blocks[1][3]), B_blocks[4][0]), B_blocks[4][2]), B_blocks[4][3])
        )

        self.h[65] = self.ai(
            self.add_matrices(
                self.subtract_matrices(
                    self.add_matrices(
                        self.subtract_matrices(
                            self.subtract_matrices(
                                self.subtract_matrices(
                                    self.subtract_matrices(
                                        self.add_matrices(
                                            self.subtract_matrices(A_blocks[0][0], A_blocks[0][1]),
                                            A_blocks[0][2]
                                        ),
                                        A_blocks[0][4]
                                    ), A_blocks[1][1]), A_blocks[1][4]), A_blocks[2][1]), A_blocks[2][2]),
                    A_blocks[3][0]),
                A_blocks[3][1]),

            B_blocks[1][3]
        )

        self.h[66] = self.ai(
            self.subtract_matrices(A_blocks[1][4], A_blocks[2][4]),
            self.add_matrices(
                self.add_matrices(self.subtract_matrices(
                    self.subtract_matrices(
                        self.subtract_matrices(
                            self.subtract_matrices(
                                self.add_matrices(
                                    self.add_matrices(B_blocks[0][0], B_blocks[0][1]),
                                    B_blocks[0][4]), B_blocks[1][4]), B_blocks[3][0]), B_blocks[3][1]), B_blocks[3][4]),
                    B_blocks[4][1]), B_blocks[4][4])

        )

        self.h[67] = self.ai(
            self.add_matrices(
                self.add_matrices(
                    self.subtract_matrices(
                        self.subtract_matrices(
                            self.subtract_matrices(
                                self.subtract_matrices(
                                    self.add_matrices(A_blocks[0][0], A_blocks[0][2]), A_blocks[0][3]), A_blocks[0][4]),
                            A_blocks[3][0]), A_blocks[3][2]), A_blocks[3][3]), A_blocks[3][4]),

            self.add_matrices(self.subtract_matrices(self.negate_matrix(B_blocks[2][0]), B_blocks[2][2]),
                              B_blocks[2][3]
                              )
        )

        self.h[68] = self.ai(
            self.add_matrices(
                self.subtract_matrices(
                    self.add_matrices(self.negate_matrix(A_blocks[0][2]), A_blocks[0][3]),
                    A_blocks[1][2]), A_blocks[1][3]),

            self.add_matrices(
                self.subtract_matrices(
                    self.add_matrices(
                        self.subtract_matrices(
                            self.subtract_matrices(self.negate_matrix(B_blocks[1][3]), B_blocks[2][0]),
                            B_blocks[2][1]), B_blocks[2][3]), B_blocks[4][1]), B_blocks[4][3]))

        self.h[69] = self.ai(
            self.subtract_matrices(
                self.add_matrices(
                    self.add_matrices(A_blocks[1][2], self.negate_matrix(A_blocks[1][4])),
                    A_blocks[3][2]
                ),
                A_blocks[3][4]
            ),
            self.negate_matrix(
                self.add_matrices(
                    self.add_matrices(B_blocks[2][0], B_blocks[2][1]),
                    B_blocks[2][2]
                )
            )
        )

        self.h[70] = self.ai(
            self.add_matrices(
                self.subtract_matrices(
                    self.add_matrices(
                        self.subtract_matrices(
                            self.add_matrices(
                                self.subtract_matrices(
                                    self.add_matrices(self.negate_matrix(A_blocks[2][0]), A_blocks[2][2]),
                                    A_blocks[2][3]
                                ),
                                A_blocks[2][4]
                            ), A_blocks[3][0]), A_blocks[3][2]), A_blocks[3][3]), A_blocks[3][4]),

            self.negate_matrix(
                self.add_matrices(
                    self.add_matrices(B_blocks[4][0], B_blocks[4][2]),
                    B_blocks[4][4]
                )
            )
        )

        self.h[71] = self.ai(self.subtract_matrices(
            self.subtract_matrices(self.subtract_matrices(self.negate_matrix(A_blocks[1][0]), A_blocks[1][3]),
                                   A_blocks[3][0]), A_blocks[3][3]),
                             self.add_matrices(self.add_matrices(B_blocks[3][0], B_blocks[3][1]), B_blocks[3][2]))

        self.h[72] = self.ai(
            self.subtract_matrices(
                self.subtract_matrices(
                    self.add_matrices(
                        self.subtract_matrices(
                            self.subtract_matrices(
                                A_blocks[0][2], A_blocks[0][3]), A_blocks[0][4]), A_blocks[1][2]), A_blocks[1][3]),
                A_blocks[1][4]),
            self.subtract_matrices(
                self.add_matrices(
                    self.add_matrices(
                        self.subtract_matrices(
                            self.add_matrices(B_blocks[0][0], B_blocks[0][1]), B_blocks[0][3]), B_blocks[1][3]),
                    B_blocks[4][1]), B_blocks[4][3])

        )

        self.h[73] = self.ai(self.subtract_matrices(self.add_matrices(self.subtract_matrices(
            self.add_matrices(self.subtract_matrices(A_blocks[1][0], A_blocks[1][2]), A_blocks[1][3]), A_blocks[2][0]),
                                                                      A_blocks[2][2]), A_blocks[2][3]),

                             self.add_matrices(self.add_matrices(B_blocks[3][0], B_blocks[3][1]), B_blocks[3][4]))

        self.h[74] = self.ai(
            self.add_matrices(
                self.subtract_matrices(
                    self.add_matrices(
                        self.add_matrices(
                            self.add_matrices(
                                self.subtract_matrices(
                                    self.subtract_matrices(
                                        self.subtract_matrices(
                                            self.add_matrices(A_blocks[0][1], A_blocks[0][3]),
                                            A_blocks[1][1]), A_blocks[1][4]), A_blocks[2][0]), A_blocks[2][1]),
                            A_blocks[2][3]), A_blocks[2][4]), A_blocks[3][0]),
                A_blocks[3][1]),

            B_blocks[1][4]
        )

        self.h[75] = self.ai(self.add_matrices(A_blocks[0][2], A_blocks[2][2]),
                             self.subtract_matrices(self.add_matrices(self.add_matrices(self.subtract_matrices(
                                 self.add_matrices(self.negate_matrix(B_blocks[0][0]), B_blocks[0][3]), B_blocks[0][4]),
                                                                                        B_blocks[1][3]),
                                                                      B_blocks[2][3]), B_blocks[2][4]))

        for i in range(76):
            self.h[i] = self.h[i][0]

        C[0][0] = -self.h[9][0] + self.h[11][0] + self.h[13][0] - self.h[14][0] - self.h[15][0] + self.h[52][0] + \
                  self.h[4][0] - self.h[65][0] - self.h[6][0]
        C[1][0] = self.h[9][0] + self.h[10][0] - self.h[11][0] + self.h[12][0] + self.h[14][0] + self.h[15][0] - \
                  self.h[16][0] - self.h[43][0] + self.h[50][0]
        C[2][0] = self.h[9][0] - self.h[11][0] + self.h[14][0] + self.h[15][0] - self.h[0][0] + self.h[1][0] + \
                  self.h[2][0] - self.h[3][0] + self.h[74][0]
        C[3][0] = -self.h[9][0] + self.h[11][0] - self.h[14][0] - self.h[15][0] + self.h[51][0] + self.h[53][0] - \
                  self.h[5][0] - self.h[7][0] + self.h[8][0]
        C[0][1] = self.h[12][0] + self.h[14][0] + self.h[19][0] + self.h[20][0] - self.h[21][0] + self.h[22][0] + \
                  self.h[24][0] - self.h[42][0] + self.h[48][0] + self.h[49][0]
        C[1][1] = -self.h[10][0] + self.h[11][0] - self.h[12][0] - self.h[14][0] - self.h[15][0] + self.h[16][0] + \
                  self.h[17][0] - self.h[18][0] - self.h[20][0] + self.h[42][0] + self.h[43][0]
        C[2][1] = -self.h[15][0] - self.h[18][0] - self.h[20][0] - self.h[27][0] - self.h[28][0] - self.h[37][0] + \
                  self.h[41][0] + self.h[43][0] - self.h[46][0] + self.h[47][0]
        C[3][1] = self.h[10][0] - self.h[11][0] - self.h[17][0] + self.h[20][0] - self.h[31][0] + self.h[32][0] - \
                  self.h[33][0] - self.h[35][0] + self.h[61][0] - self.h[69][0]
        C[0][2] = self.h[14][0] + self.h[22][0] + self.h[23][0] + self.h[33][0] - self.h[36][0] + self.h[39][0] - \
                  self.h[40][0] + self.h[54][0] - self.h[55][0] - self.h[8][0]
        C[1][2] = -self.h[9][0] + self.h[18][0] + self.h[31][0] + self.h[34][0] + self.h[35][0] + self.h[36][0] - \
                  self.h[42][0] - self.h[59][0] - self.h[5][0] - self.h[71][0]
        C[2][2] = -self.h[15][0] - self.h[27][0] + self.h[32][0] + self.h[36][0] - self.h[38][0] + self.h[44][0] - \
                  self.h[45][0] + self.h[62][0] - self.h[70][0] - self.h[7][0]
        C[3][2] = self.h[9][0] + self.h[14][0] + self.h[15][0] - self.h[32][0] + self.h[33][0] - self.h[34][0] - \
                  self.h[36][0] - self.h[53][0] + self.h[5][0] + self.h[7][0] - self.h[8][0]
        C[0][3] = -self.h[9][0] + self.h[11][0] + self.h[13][0] - self.h[15][0] + self.h[22][0] + self.h[23][0] + \
                  self.h[24][0] + self.h[25][0] + self.h[4][0] - self.h[65][0] - self.h[6][0]
        C[1][3] = self.h[9][0] + self.h[17][0] - self.h[18][0] + self.h[19][0] - self.h[21][0] - self.h[23][0] - \
                  self.h[25][0] - self.h[4][0] - self.h[68][0] + self.h[72][0]
        C[2][3] = -self.h[13][0] + self.h[15][0] - self.h[22][0] - self.h[25][0] + self.h[26][0] + self.h[28][0] + \
                  self.h[30][0] + self.h[45][0] - self.h[57][0] + self.h[75][0]
        C[3][3] = self.h[11][0] + self.h[24][0] + self.h[25][0] - self.h[32][0] - self.h[34][0] - self.h[39][0] + \
                  self.h[40][0] + self.h[64][0] - self.h[67][0] - self.h[6][0]
        C[0][4] = self.h[14][0] + self.h[23][0] + self.h[24][0] + self.h[26][0] - self.h[27][0] + self.h[29][0] + \
                  self.h[30][0] - self.h[3][0] + self.h[60][0] + self.h[63][0]
        C[1][4] = -self.h[9][0] - self.h[17][0] - self.h[1][0] - self.h[29][0] - self.h[37][0] + self.h[41][0] - \
                  self.h[42][0] + self.h[45][0] + self.h[66][0] + self.h[73][0]
        C[2][4] = -self.h[9][0] + self.h[11][0] - self.h[14][0] + self.h[27][0] + self.h[28][0] - self.h[1][0] - \
                  self.h[29][0] - self.h[2][0] + self.h[45][0] + self.h[3][0] - self.h[74][0]
        C[3][4] = -self.h[11][0] - self.h[28][0] + self.h[29][0] - self.h[33][0] + self.h[34][0] + self.h[38][0] + \
                  self.h[2][0] - self.h[44][0] + self.h[56][0] + self.h[58][0]

        return self.fill_matrix(C, m, k, m // 4, k // 5)


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
ai_inst = AIALGORITHM()
result = ai_inst.ai(A1, B1)
result2 = ai_inst.multiply_matrices(A1, B1)
print(result)
print(result2)
assert result2 == result, "Error"