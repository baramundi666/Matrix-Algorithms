from tests.test_ai_algorithm import TestAIAlgorithm
from tests.test_binet_algorithm import TestBinetAlgorithm
from tests.test_strassen_algorithm import TestStrassenAlgorithm


def main():
    tests = [TestStrassenAlgorithm(), TestBinetAlgorithm(), TestAIAlgorithm()]
    for test in tests:
        test.run()

if __name__ == "__main__":
    main()