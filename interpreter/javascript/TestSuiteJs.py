import json
import subprocess

from interpreter.TestSuite import TestSuite
from interpreter.javascript.json_helper import stringify, stringify_actor_definitions, stringify_steps


def execute(cmd):
    popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ''):
        yield stdout_line
    popen.stdout.close()
    exitcode = popen.wait()
    if exitcode:
        raise subprocess.CalledProcessError(exitcode, cmd)


class TestSuiteJs(TestSuite):
    def __init__(self, helper_path, verbose=False):
        super().__init__(verbose)
        self.helper_path = helper_path

    def run_all(self):
        self.run_tests(self.tests)

    def run_test(self, test_name, single=True):
        str_test = stringify(test_name)
        single_test = {str_test: self.tests[str_test]}
        self.run_tests(single_test)

    def run_tests(self, test_list):
        node_cmd = r'node {} "{}" "{}" "{}" "{}" "{}" "{}" "{}"'.format(
            self.helper_path, json.dumps(self.global_actor_definitions), json.dumps(self.before_all),
            json.dumps(self.befores), json.dumps(test_list), json.dumps(self.afters),
            json.dumps(self.after_all), str(self.verbose)
        )
        for line in execute(node_cmd):
            if 'test_report' in line:
                self.test_report = json.loads(line)['test_report']
            else:
                print(line, end='')

    def set_global_actor_definitions(self, model):
        self.global_actor_definitions = stringify_actor_definitions(model.global_actors)

    def set_before_all(self, model):
        self.before_all = stringify_steps(model.before_all.ba_steps, self.model)

    def set_befores(self, model):
        self.befores = {stringify(bb.name): stringify_steps(bb.b_steps, self.model) for bb in model.before.b_blocks}

    def set_tests(self, model):
        self.tests = {
            stringify(test.name): [
                stringify_actor_definitions(test.actors),
                [stringify(b.name) for b in test.befores],
                stringify_steps(test.e_steps, self.model),
                [stringify(a.name) for a in test.afters],
            ] for test in model.tests
        }

    def set_afters(self, model):
        self.afters = {stringify(ab.name): stringify_steps(ab.a_steps, self.model) for ab in model.after.a_blocks}

    def set_after_all(self, model):
        self.after_all = stringify_steps(model.after_all.aa_steps, self.model)
