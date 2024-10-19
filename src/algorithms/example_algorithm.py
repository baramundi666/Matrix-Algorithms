from base_algorithm import BaseAlgorithm


class ExampleAlgorithm(BaseAlgorithm):
    def run(self, matrix1, matrix2):
        print(self.name)
        print(matrix1, matrix2)