import os

from dsl.metamodel import get_metamodel
from interpreter.TestPy import TestSuite

if __name__ == '__main__':
    meta = get_metamodel()
    model = meta.model_from_file(os.getcwd() + '/dsl/test/models/model_big.test')

    test_suite = TestSuite(verbose=False)
    test_suite.interpret(model)
    print(test_suite)

    # single test
    test_suite.run_test('databaseQueries')
    print(test_suite)
    # all tests
    test_suite.run_all()
    print(test_suite)