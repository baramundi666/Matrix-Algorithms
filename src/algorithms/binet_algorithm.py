from src.base_algorithm import BaseAlgorithm


class BinetAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.matrix_3 = None

    #metoda wykonująca algorytm Binet
    def __binet(self, A, B):
        n = len(A)
        if n == 1:
            return self.calculator.multiply_one_by_one_matrices(A, B)

        A11, A12, A21, A22 = self.calculator.split_into_block_matrices(A)
        B11, B12, B21, B22 = self.calculator.split_into_block_matrices(B)

        C11 = self.calculator.add(self.__binet(A11, B11), self.__binet(A12, B21))
        C12 = self.calculator.add(self.__binet(A11, B12), self.__binet(A12, B22))
        C21 = self.calculator.add(self.__binet(A21, B11), self.__binet(A22, B21))
        C22 = self.calculator.add(self.__binet(A21, B12), self.__binet(A22, B22))

        return self.calculator.connect_block_matrices(C11, C12, C21, C22)

    def run(self, A, B):
        self.matrix_3 = self.__binet(A, B)




