from test.utils import run_py, run_js


def test_everything_ok():
    test_suite_py = run_py('model_everything_ok.test')

    assert 0 == len(test_suite_py.test_report['BA'])
    assert 3 == test_suite_py.test_report['TC']
    assert 3 == len(test_suite_py.test_report['ST'])
    assert 0 == len(test_suite_py.test_report['FT'])
    assert 0 == len(test_suite_py.test_report['AA'])

    test_suite_js = run_js('model_everything_ok.test')

    assert 0 == len(test_suite_js.test_report['BA'])
    assert 3 == test_suite_js.test_report['TC']
    assert 3 == len(test_suite_js.test_report['ST'])
    assert 0 == len(test_suite_js.test_report['FT'])
    assert 0 == len(test_suite_js.test_report['AA'])


def test_error_in_ba_and_aa():
    test_suite_py = run_py('model_error_in_ba_and_aa.test')

    assert 1 ==  len(test_suite_py.test_report['BA'])
    assert 1 ==  test_suite_py.test_report['TC']
    assert 1 ==  len(test_suite_py.test_report['AA'])

    test_suite_js = run_js('model_error_in_ba_and_aa.test')

    assert 1 == len(test_suite_js.test_report['BA'])
    assert 1 == test_suite_js.test_report['TC']
    assert 1 == len(test_suite_js.test_report['AA'])


def test_error_in_b_and_a():
    test_suite_py = run_py('model_error_in_b_and_a.test')

    assert 1 == test_suite_py.test_report['TC']
    assert 0 == len(test_suite_py.test_report['ST'])
    assert 1 == len(test_suite_py.test_report['FT'])

    test_suite_js = run_js('model_error_in_b_and_a.test')

    assert 1 == test_suite_js.test_report['TC']
    assert 0 == len(test_suite_js.test_report['ST'])
    assert 1 == len(test_suite_js.test_report['FT'])


def test_error_in_test():
    test_suite_py = run_py('model_error_in_test.test')

    assert 1 ==  test_suite_py.test_report['TC']
    assert 0 == len(test_suite_py.test_report['ST'])
    assert 1 == len(test_suite_py.test_report['FT'])

    test_suite_js = run_js('model_error_in_test.test')

    assert 1 == test_suite_js.test_report['TC']
    assert 0 == len(test_suite_js.test_report['ST'])
    assert 1 == len(test_suite_js.test_report['FT'])
