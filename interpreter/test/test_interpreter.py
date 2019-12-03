from os.path import dirname, join

from dsl import get_metamodel
from interpreter.TestPy import TestSuite


def test_error_in_ba():
    meta = get_metamodel()
    model = meta.model_from_file(join(dirname(__file__), 'models', 'model_error_in_ba.test'))

    test_suite = TestSuite(verbose=False)
    test_suite.interpret(model)
    test_suite.run_all()

    assert 1 ==  len(test_suite.test_report['BA'])
