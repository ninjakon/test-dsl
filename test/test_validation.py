from dsl import get_metamodel
from os.path import dirname, join
from textx import get_children_of_type, TextXSemanticError
from pytest import raises


def test_validation_big():
    meta = get_metamodel()
    model = meta.model_from_file(join(dirname(__file__), 'models', 'model_big.test'))
    assert 3 == len(get_children_of_type('Test', model))


def test_validation_ok():
    meta = get_metamodel()
    model = meta.model_from_file(join(dirname(__file__), 'models', 'model_ok.test'))
    assert 1 == len(get_children_of_type('Test', model))


def test_validation_not_ok():
    meta = get_metamodel()
    with raises(TextXSemanticError):
        meta.model_from_file(join(dirname(__file__), 'models', 'model_not_ok.test'))
