from os.path import dirname, join

from dsl import get_metamodel
from interpreter.TestSuitePy import TestSuitePy


def test_everything_ok():
    meta = get_metamodel()
    model = meta.model_from_file(join(dirname(__file__), 'models', 'model_everything_ok.test'))

    test_suite = TestSuitePy(verbose=False)
    test_suite.interpret(model)
    test_suite.run_all()

    assert 0 == len(test_suite.test_report['BA'])
    assert 3 == test_suite.test_report['TC']
    assert 3 == len(test_suite.test_report['ST'])
    assert 0 == len(test_suite.test_report['FT'])
    assert 0 == len(test_suite.test_report['AA'])


def test_error_in_ba_and_aa():
    meta = get_metamodel()
    model = meta.model_from_file(join(dirname(__file__), 'models', 'model_error_in_ba_and_aa.test'))

    test_suite = TestSuitePy(verbose=False)
    test_suite.interpret(model)
    test_suite.run_all()

    assert 1 ==  len(test_suite.test_report['BA'])
    assert 1 ==  test_suite.test_report['TC']
    assert 1 ==  len(test_suite.test_report['AA'])


def test_error_in_b_and_a():
    meta = get_metamodel()
    model = meta.model_from_file(join(dirname(__file__), 'models', 'model_error_in_b_and_a.test'))

    test_suite = TestSuitePy(verbose=False)
    test_suite.interpret(model)
    test_suite.run_all()

    assert 1 == test_suite.test_report['TC']
    assert 0 == len(test_suite.test_report['ST'])
    assert 1 == len(test_suite.test_report['FT'])


def test_error_in_test():
    meta = get_metamodel()
    model = meta.model_from_file(join(dirname(__file__), 'models', 'model_error_in_test.test'))

    test_suite = TestSuitePy(verbose=False)
    test_suite.interpret(model)
    test_suite.run_all()

    assert 1 ==  test_suite.test_report['TC']
    assert 0 == len(test_suite.test_report['ST'])
    assert 1 == len(test_suite.test_report['FT'])
