import datetime
import pandas as pd

from tests.test_ai_algorithm import TestAIAlgorithm
from tests.test_binet_algorithm import TestBinetAlgorithm
from tests.test_gauss_algorithm import TestGaussAlgorithm
from tests.test_strassen_algorithm import TestStrassenAlgorithm
from tests.test_inversion import TestInversion
from tests.test_lu import TestLU



def main():
    test = TestInversion()
    test.run()
    write_data_to_file(test.data, f"{test.algorithm}-n{test.n}-")


def write_data_to_file(data, name):
    df = pd.DataFrame(data=data, index=["time", "flop"])
    time_snapshot = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    df.to_csv("data/" + name)


if __name__ == "__main__":
    main()