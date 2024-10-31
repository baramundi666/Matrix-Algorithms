from src.calculator import Calculator


class BaseAlgorithm:
    def __init__(self):
        self.name = self.__class__.__name__
        self.calc = Calculator()

    def run(self, *args):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name