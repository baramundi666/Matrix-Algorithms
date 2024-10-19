from timeit import default_timer as timer
from datetime import timedelta

from base_algorithm import BaseAlgorithm


class BaseAlgorithmTest:
    def __init__(self):
        self.algorithm = BaseAlgorithm()

    def run(self):
        pass

    def _run_time_test(self, test_info: str, *args):
        print(f"Running {self.algorithm}: {test_info}")
        # time start
        start = timer()
        # run algorithm
        self.algorithm.run(*args)
        # time end
        end = timer()
        print(f"Time: {timedelta(seconds=end - start)}")

    def _extract_calculator_data(self):
        print(f"Atomic additions: {self.algorithm.calculator.add_count}")
        print(f"Atomic subtractions: {self.algorithm.calculator.subtract_count}")
        print(f"Atomic negations: {self.algorithm.calculator.negate_count}")
        print(f"Atomic multiplications: {self.algorithm.calculator.multiply_count}")
        self.algorithm.calculator.reset_counters()

    @classmethod
    def generate_data(cls, *args):
        pass
