import sys, getopt, os

from dsl.metamodel import get_metamodel
from interpreter.TestSuitePy import TestSuitePy


def print_help():
    print('test-dsl -t <test_suite_file> -v -a -s <test1/test2/...>')


def run(argv):
    test_suite_file = ''
    verbose = False
    single_tests = []
    run_all = False

    try:
        opts, args = getopt.getopt(argv, 'ht:vas:', ['help', 'test-suite=', 'verbose=', 'run-all', 'run-single'])
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

    if not os.path.isfile(test_suite_file):
        print('File "' + test_suite_file + '" does not exist.')
        sys.exit(2)

    # create model
    meta = get_metamodel()
    model = meta.model_from_file(test_suite_file)

    # register test suite
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
