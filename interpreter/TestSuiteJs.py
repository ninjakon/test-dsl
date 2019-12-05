import json

from Naked.toolshed.shell import muterun_js

from interpreter.TestSuite import TestSuite


def stringify(string):
    if not isinstance(string, str): return string
    return '"' + str(string) + '"'


class TestSuiteJs(TestSuite):
    def run_all(self):
        response = muterun_js('interpreter/TestHelper.js', '"' + json.dumps(self.actor_definitions) + '"')
        if response.exitcode == 0:
            print(response.stdout.decode("utf-8"))
        else:
            print(response.stderr.decode("utf-8"))

    def run_test(self, test_name, single=True):
        pass

    def set_actor_definition(self, actor):
        module = actor.path.replace('-', '/')
        actor_class = '../' + module + '.js'
        class_name = actor.class_name
        self.actor_definitions[stringify(actor.name)] = \
            ((stringify(actor_class), stringify(class_name)),
             [(stringify(a.name), stringify(a.value)) for a in actor.attributes])

    def set_before_alls(self, model):
        pass

    def set_befores(self, model):
        pass

    def set_tests(self, model):
        pass

    def set_afters(self, model):
        pass

    def set_after_alls(self, model):
        pass
