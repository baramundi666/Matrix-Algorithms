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


    def _extract_calc_data(self):
        # print(f"Atomic additions: {self.algorithm.calc.add_count}")
        # print(f"Atomic subtractions: {self.algorithm.calc.subtract_count}")
        # print(f"Atomic negations: {self.algorithm.calc.negate_count}")
        # print(f"Atomic multiplications: {self.algorithm.calc.multiply_count}")
        # print(f"Atomic divisions: {self.algorithm.calc.divide_count}")
        total_count = self.algorithm.calc.total_count
        print(f"FLOP: {total_count}")
        self.algorithm.calc.reset_counters()
        self.algorithm.reset_helper_calculators()
        return total_count

    @classmethod
    def generate_data(cls, *args):
        pass
