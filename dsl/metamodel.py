from textx import metamodel_from_file
from textx.scoping.providers import PlainName, RelativeName
from os.path import dirname, abspath, join


def get_metamodel():
    dir = dirname(abspath(__file__))
    meta_model = metamodel_from_file(join(dir, 'test-dsl.tx'))

    meta_model.register_scope_providers({
        'CallStep.actor': PlainName(multi_metamodel_support=False),
        'AttributeReference.actor': PlainName(multi_metamodel_support=False),
        'AttributeReference.attribute': PlainName(multi_metamodel_support=False)
    })

    return meta_model
