import json

from Naked.toolshed.shell import muterun_js

from interpreter.TestSuite import TestSuite


class TestSuiteJs(TestSuite):
    def run_all(self):
        response = muterun_js('interpreter/TestHelper.js', '"' + json.dumps(self.actor_definitions) + '"')
        print(response.stdout.decode("utf-8"))

    def run_test(self, test_name, single=True):
        pass

    def set_actor_definition(self, actor):
        module = actor.path.replace('-', '/')
        class_name = actor.class_name
        actor_class = '../' + module + '.js'
        self.actor_definitions[actor.name] = (actor_class, [(a.name, a.value) for a in actor.attributes])

