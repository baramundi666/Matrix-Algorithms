from src.calculator import Calculator


class BaseAlgorithm:
    def __init__(self):
        self.name = self.__class__.__name__
        self.calc = Calculator()
        self.calcs = list()

    def run(self, *args):
        pass

    def reset_helper_calculators(self):
        for calc in self.calcs:
            calc.reset_counters()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name