import json

from Naked.toolshed.shell import muterun_js

from interpreter.TestSuite import TestSuite


def stringify(string):
    if not isinstance(string, str): return string
    return '"' + str(string) + '"'


def stringify_steps(steps):
    return [stringify_step(s) for s in steps]


def stringify_step(step):
    step_type = step.__class__.__name__
    step_vars = []
    if step_type == 'AssignStep':
        step_vars.append(stringify(step.attributeReference.actor.name))
        step_vars.append(stringify(step.attributeReference.attribute.name))
        step_vars.append(stringify(step.value))
    elif step_type == 'CallStep':
        step_vars.append(stringify(step.actor.name))
        step_vars.append(stringify(step.method))
        parameters = [(False, p.value) if p.actor is None else (True, stringify(p.actor.name)) for p in step.parameters]
        step_vars.append(parameters)
    elif step_type == 'AssertStep':
        step_vars.append(stringify(step.attributeReference.actor.name))
        step_vars.append(stringify(step.attributeReference.attribute.name))
        step_vars.append(stringify(step.value))
    elif step_type == 'TimeStep':
        step_vars.append(step.delay)
    return [stringify(step_type), step_vars]


class TestSuiteJs(TestSuite):
    def run_all(self):
        response = muterun_js(
            'interpreter/TestHelper.js',
            '"' + json.dumps(self.actor_definitions) + '"' + ' '
            '"' + json.dumps(self.before_alls) + '"' + ' ' +
            '"' + json.dumps(self.befores) + '"' + ' ' +
            '"' + json.dumps(self.tests) + '"' + ' ' +
            '"' + json.dumps(self.afters) + '"' + ' ' +
            '"' + json.dumps(self.after_alls) + '"' + ' ' +
            '"' + str(self.verbose) + '"'
        )
        if response.exitcode == 0:
            print(response.stdout.decode("utf-8"))
        else:
            print(response.stderr.decode("utf-8"))

    def run_test(self, test_name, single=True):
        pass

    def set_actor_definitions(self, model):
        for actor in model.actors:
            module = actor.path.replace('-', '/')
            actor_class = '../' + module + '.js'
            self.actor_definitions[stringify(actor.name)] = \
                (stringify(actor_class), [(stringify(a.name), stringify(a.value)) for a in actor.attributes])

    def set_before_all(self, model):
        self.before_alls = stringify_steps(model.before_all.ba_steps)

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
        self.after_alls = stringify_steps(model.after_all.aa_steps)
