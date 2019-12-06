import sys, getopt, os

from enum import Enum

from dsl.metamodel import get_metamodel
from interpreter.python.TestSuitePy import TestSuitePy
from interpreter.javascript.TestSuiteJs import TestSuiteJs


class SupportedLanguages(Enum):
    PYTHON = 0
    JAVASCRIPT = 1


def print_help():
    print('test-dsl -t <test_suite_file> -v -a -s <test1/test2/...> -l <py|js>')


def run(argv):
    test_suite_file = ''
    verbose = False
    single_tests = []
    run_all = False
    language = SupportedLanguages.PYTHON

    try:
        opts, args = getopt.getopt(argv, 'ht:vas:l:',
                                   ['help', 'test-suite=', 'verbose=', 'run-all', 'run-single', 'language='])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ('-t', '--test-suite'):
            test_suite_file = arg
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-a', '--run-all'):
            run_all = True
        elif opt in ('-s', '--run-single'):
            single_tests = arg.split('/')
        elif opt in ('-l', '--language'):
            if arg == 'py':
                language = SupportedLanguages.PYTHON
            elif arg == 'js':
                language = SupportedLanguages.JAVASCRIPT
            else:
                print_help()
                sys.exit(1)

    if not os.path.isfile(test_suite_file):
        print('File "' + test_suite_file + '" does not exist.')
        sys.exit(2)

    # create model
    meta = get_metamodel()
    model = meta.model_from_file(test_suite_file)

    # register test suite
    if language == SupportedLanguages.JAVASCRIPT:
        test_suite = TestSuiteJs('./interpreter/javascript/TestHelper.js', verbose=verbose)
    else:
        test_suite = TestSuitePy(verbose=verbose)
    test_suite.interpret(model)
    print('Registered test suite successfully.\n')

    # run single tests
    for test in single_tests:
        test_suite.run_test(test)
        print(test_suite)

    # run all tests
    if run_all:
        test_suite.run_all()
        print(test_suite)


if __name__ == '__main__':
    run(sys.argv[1:])
