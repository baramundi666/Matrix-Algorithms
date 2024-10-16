from timeit import default_timer as timer
from datetime import timedelta

from src.base_algorithm import BaseAlgorithm


class BaseAlgorithmTest:
    def __init__(self):
        self.algorithm = BaseAlgorithm()

    def run(self):
        pass

    def _run_time_test(self, test_size: int, *args):
        print(f"Running {self.algorithm} with testing size: {test_size}")
        # time start
        start = timer()
        # run algorithm
        self.algorithm.run(*args)
        # time end
        end = timer()
        print(f"Time: {timedelta(seconds=end - start)}")

    @classmethod
    def generate_data(cls, *args):
        pass
