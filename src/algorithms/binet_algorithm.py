from src.base_algorithm import BaseAlgorithm


class BinetAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.matrix_3 = None

    #dzielenie macierzy na 4 podmacierze
    def split_matrix(self, M):
        n = len(M) // 2
        A11 = [row[:n] for row in M[:n]]
        A12 = [row[n:] for row in M[:n]]
        A21 = [row[:n] for row in M[n:]]
        A22 = [row[n:] for row in M[n:]]
        return A11, A12, A21, A22

    #dodawanie dwóch macierzy
    def add_matrices(self, A, B):
        return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    #metoda wykonująca algorytm Binet
    def binet(self, A, B):
        n = len(A)
        if n == 1:
            return [[A[0][0] * B[0][0]]]

        A11, A12, A21, A22 = self.split_matrix(A)
        B11, B12, B21, B22 = self.split_matrix(B)

        C11 = self.add_matrices(self.binet(A11, B11), self.binet(A12, B21))
        C12 = self.add_matrices(self.binet(A11, B12), self.binet(A12, B22))
        C21 = self.add_matrices(self.binet(A21, B11), self.binet(A22, B21))
        C22 = self.add_matrices(self.binet(A21, B12), self.binet(A22, B22))

        M1 = [C11[i] + C12[i] for i in range(len(C11))]
        M2 = [C21[i] + C22[i] for i in range(len(C21))]
        return M1 + M2

    def run(self, A, B):
        self.matrix_3 = self.binet(A, B)




