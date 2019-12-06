from test.utils import run_py, run_js

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #Interesting Tests

def test_everything_ok_py():
    test_suite_py = run_py('interpreter/interesting/model_everything_ok.test')

    assert 0 == len(test_suite_py.test_report['BA'])
    assert 3 == test_suite_py.test_report['TC']
    assert 3 == len(test_suite_py.test_report['ST'])
    assert 0 == len(test_suite_py.test_report['FT'])
    assert 0 == len(test_suite_py.test_report['AA'])


def test_everything_ok_js():
    test_suite_js = run_js('interpreter/interesting/model_everything_ok.test')

    assert 0 == len(test_suite_js.test_report['BA'])
    assert 3 == test_suite_js.test_report['TC']
    assert 3 == len(test_suite_js.test_report['ST'])
    assert 0 == len(test_suite_js.test_report['FT'])
    assert 0 == len(test_suite_js.test_report['AA'])

def test_everything_not_ok_py():
    test_suite_py = run_py('interpreter/interesting/model_everything_not_ok.test')

    assert 0 == len(test_suite_py.test_report['BA'])
    assert 3 == test_suite_py.test_report['TC']
    assert 1 == len(test_suite_py.test_report['ST'])
    assert 2 == len(test_suite_py.test_report['FT'])
    assert 0 == len(test_suite_py.test_report['AA'])


def test_everything_not_ok_js():
    test_suite_js = run_js('interpreter/interesting/model_everything_not_ok.test')

    assert 0 == len(test_suite_js.test_report['BA'])
    assert 3 == test_suite_js.test_report['TC']
    assert 1 == len(test_suite_js.test_report['ST'])
    assert 2 == len(test_suite_js.test_report['FT'])
    assert 0 == len(test_suite_js.test_report['AA'])

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Boring Tests

def test_error_in_ba_and_aa_py():
    test_suite_py = run_py('interpreter/boring/model_error_in_ba_and_aa.test')

    assert 1 ==  len(test_suite_py.test_report['BA'])
    assert 1 ==  test_suite_py.test_report['TC']
    assert 1 ==  len(test_suite_py.test_report['AA'])


def test_error_in_ba_and_aa_js():
    test_suite_js = run_js('interpreter/boring/model_error_in_ba_and_aa.test')

    assert 1 == len(test_suite_js.test_report['BA'])
    assert 1 == test_suite_js.test_report['TC']
    assert 1 == len(test_suite_js.test_report['AA'])


def test_error_in_b_and_a_py():
    test_suite_py = run_py('interpreter/boring/model_error_in_b_and_a.test')

    assert 1 == test_suite_py.test_report['TC']
    assert 0 == len(test_suite_py.test_report['ST'])
    assert 1 == len(test_suite_py.test_report['FT'])


def test_error_in_b_and_a_js():
    test_suite_js = run_js('interpreter/boring/model_error_in_b_and_a.test')

    assert 1 == test_suite_js.test_report['TC']
    assert 0 == len(test_suite_js.test_report['ST'])
    assert 1 == len(test_suite_js.test_report['FT'])


def test_error_in_test_py():
    test_suite_py = run_py('interpreter/boring/model_error_in_test.test')

    assert 1 ==  test_suite_py.test_report['TC']
    assert 0 == len(test_suite_py.test_report['ST'])
    assert 1 == len(test_suite_py.test_report['FT'])


def test_error_in_test_js():
    test_suite_js = run_js('interpreter/boring/model_error_in_test.test')

    assert 1 == test_suite_js.test_report['TC']
    assert 0 == len(test_suite_js.test_report['ST'])
    assert 1 == len(test_suite_js.test_report['FT'])
