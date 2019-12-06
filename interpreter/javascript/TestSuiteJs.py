import json

from Naked.toolshed.shell import muterun_js

from interpreter.TestSuite import TestSuite
from interpreter.javascript.json_helper import stringify, stringify_steps


class TestSuiteJs(TestSuite):
    def __init__(self, helper_path, verbose=False):
        super().__init__(verbose)
        self.helper_path = helper_path

    def run_all(self):
        self.run_tests(self.tests)

    def run_test(self, test_name, single=True):
        str_test = stringify(test_name)
        single_test = { str_test: self.tests[str_test] }
        self.run_tests(single_test)

    def run_tests(self, test_list):
        response = muterun_js(
            self.helper_path,
            '"' + json.dumps(self.actor_definitions) + '"' + ' '
                                                             '"' + json.dumps(self.before_all) + '"' + ' ' +
            '"' + json.dumps(self.befores) + '"' + ' ' +
            '"' + json.dumps(test_list) + '"' + ' ' +
            '"' + json.dumps(self.afters) + '"' + ' ' +
            '"' + json.dumps(self.after_all) + '"' + ' ' +
            '"' + str(self.verbose) + '"'
        )
        if response.exitcode == 0:
            response_dict = json.loads(response.stdout.decode("utf-8"))
            self.print_log(response_dict['log'])
        else:
            print(response.stderr.decode("utf-8"))

    def set_actor_definitions(self, model):
        for actor in model.actors:
            module = actor.path.replace('-', '/')
            actor_class = '../../' + module + '.js'
            self.actor_definitions[stringify(actor.name)] = \
                (stringify(actor_class), [(stringify(a.name), stringify(a.value)) for a in actor.attributes])

    def set_before_all(self, model):
        self.before_all = stringify_steps(model.before_all.ba_steps)

    def set_befores(self, model):
        self.befores = {stringify(bb.name): stringify_steps(bb.b_steps) for bb in model.before.b_blocks}

    def set_tests(self, model):
        self.tests = {
            stringify(test.name): [
                [stringify(b.name) for b in test.befores],
                stringify_steps(test.e_steps),
                [stringify(a.name) for a in test.afters],
            ] for test in model.tests
        }

    def set_afters(self, model):
        self.afters = {stringify(ab.name): stringify_steps(ab.a_steps) for ab in model.after.a_blocks}

    def set_after_all(self, model):
        self.after_all = stringify_steps(model.after_all.aa_steps)

    def print_log(self, log):
        actor_table = log['actor_table']
        if self.verbose and len(actor_table) > 0:
            print()
            print(self.instance_row.format('Instance', 'Class', 'Attributes'))
            print(self.instance_row.format('-' * 15, '-' * 31, '-' * 127))
            for actor in actor_table:
                print(self.instance_row.format(str(actor[0]), str(actor[1]), str(actor[2])))
            print()
        print(log['raw_text'])
