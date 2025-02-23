import datetime

import numpy as np
import pandas as pd

from src.algorithms.det_algorithm import DetAlgorithm
from src.algorithms.gauss_algorithm import GaussAlgorithm
from tests.test_ai_algorithm import TestAIAlgorithm
from tests.test_binet_algorithm import TestBinetAlgorithm
from tests.test_det_algorithm import TestDetAlgorithm
from tests.test_gauss_algorithm import TestGaussAlgorithm
from tests.test_strassen_algorithm import TestStrassenAlgorithm
from tests.test_inversion import TestInversion
from tests.test_lu import TestLU



def main():
    # test = TestLU()
    # test.run()
    TestDetAlgorithm().run()
    #write_data_to_file(test.data, f"{test.algorithm}-n{test.n}-")


def write_data_to_file(data, name):
    df = pd.DataFrame(data=data, index=["time", "flop"])
    time_snapshot = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    df.to_csv("data/" + name)


if __name__ == "__main__":
    main()