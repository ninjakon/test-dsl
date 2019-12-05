import json

from Naked.toolshed.shell import muterun_js

from interpreter.TestSuite import TestSuite


class TestSuiteJs(TestSuite):
    def run_all(self):
        actor_definitions = json.dumps(
            {
                an : (ca[0], [(a.name, a.value) for a in ca[1]]) for an, ca in self.actor_definitions.items()
            }
        )
        response = muterun_js('interpreter/TestHelper.js', json.dumps(actor_definitions))
        print(response.stdout.decode("utf-8"))

    def run_test(self, test_name, single=True):
        pass

    @staticmethod
    def import_actor(actor_obj):
        module = actor_obj.path.replace('-', '/')
        class_name = actor_obj.class_name
        return 'const ' + class_name + ' = require(../' + module + '.js)'
