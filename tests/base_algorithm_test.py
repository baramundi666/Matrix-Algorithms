from timeit import default_timer as timer
from datetime import timedelta

from src.base_algorithm import BaseAlgorithm


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
        time_elapsed = end - start
        print(f"Time: {timedelta(seconds=time_elapsed)}")
        return time_elapsed


    def _extract_calculator_data(self):
        print(f"Atomic additions: {self.algorithm.calculator.add_count}")
        print(f"Atomic subtractions: {self.algorithm.calculator.subtract_count}")
        print(f"Atomic negations: {self.algorithm.calculator.negate_count}")
        print(f"Atomic multiplications: {self.algorithm.calculator.multiply_count}")
        print(f"Atomic divisions: {self.algorithm.calculator.divide_count}")
        total_count = self.algorithm.calculator.total_count
        self.algorithm.calculator.reset_counters()
        return total_count

    @classmethod
    def generate_data(cls, *args):
        pass
