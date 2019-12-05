from os.path import dirname, join

from dsl import get_metamodel
from interpreter.python.TestSuitePy import TestSuitePy
from interpreter.javascript.TestSuiteJs import TestSuiteJs


def run_py(file_path):
    meta = get_metamodel()
    model = meta.model_from_file(join(dirname(__file__), 'models', file_path))

    test_suite = TestSuitePy(verbose=False)
    test_suite.interpret(model)
    test_suite.run_all()

    return test_suite


def run_js(file_path):
    meta = get_metamodel()
    model = meta.model_from_file(join(dirname(__file__), 'models', file_path))

    test_suite = TestSuiteJs('../interpreter/javascript/TestHelper.js', verbose=False)
    test_suite.interpret(model)
    test_suite.run_all()

    return test_suite
