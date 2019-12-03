import time


class TText:
    INFO = '\033[94m'
    OK = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UL = '\033[4m'
    ENDC = '\033[0m'


class TestSuite:
    instance_row = '| {:<15} |  {:<15} |  {:<63} |'

    def __init__(self, verbose=False):
        # test suite attributes
        self.verbose = verbose
        self.model = None
        self.test_report = {}
        self.add_error_fun = None

        # test elements
        self.actor_definitions = {}
        self.actors = {}
        self.before_alls = []
        self.befores = {}
        self.tests = {}
        self.afters = {}
        self.after_alls = []

    def __str__(self):
        if not self.test_report:
            return TText.INFO + 'Nothing to report.' + TText.ENDC

        # get all error counts
        ba_count = len(self.test_report['BA'])
        tt_count = self.test_report['TC']
        st_count = len(self.test_report['ST'])
        ft_count = len(self.test_report['FT'])
        aa_count = len(self.test_report['AA'])

        # pretty print success/error counts (including error messages)
        report = TText.INFO + 'Processed {} Tests:\n'.format(tt_count) + TText.ENDC
        if ba_count > 0:
            report += '> ' + \
                TText.FAIL + 'BeforeAll failed!\n' + TText.ENDC
            for msg in self.test_report['BA']:
                report += '> ' + ' ' * 8 + msg[0] + '\n'
                report += '> ' + ' ' * 8 + msg[1] + '\n'
        if st_count > 0:
            report += '> ' + \
                TText.OK + 'Tests passed: ' + TText.BOLD + '{}/{}'.format(st_count, tt_count) + TText.ENDC + \
                TText.OK + ' tests.\n'.format(ft_count, tt_count) + TText.ENDC
        if ft_count > 0:
            report += '> ' + \
                TText.FAIL + 'Tests failed: ' + TText.BOLD + '{}/{}'.format(ft_count, tt_count) + TText.ENDC + \
                TText.FAIL + ' tests!\n'.format(ft_count, tt_count) + TText.ENDC
            for test, msgs in self.test_report['FT']:
                report += '> ' + ' ' * 4 + TText.FAIL + test + '\n' + TText.ENDC
                for msg in msgs:
                    report += '> ' + ' ' * 8 + msg[0] + '\n'
                    report += '> ' + ' ' * 8 + msg[1] + '\n'
        if aa_count > 0:
            report += '> ' + \
                TText.FAIL + 'AfterAll failed!\n' + TText.ENDC
            for msg in self.test_report['AA']:
                report += '> ' + ' ' * 8 + msg[0] + '\n'
                report += '> ' + ' ' * 8 + msg[1] + '\n'
        return report

    def interpret(self, model):
        # need model for error position
        self.model = model

        # register actors
        for actor in model.actors:
            # load module and actor class
            module = TestSuite.import_actor(actor)
            actor_class = getattr(module, actor.class_name)
            self.actor_definitions[actor.name] = (actor_class, actor.attributes)

        # register before all steps
        if model.before_all:
            self.before_alls = model.before_all.ba_steps

        # register before blocks
        if model.before:
            self.befores = {b_block.name: b_block.b_steps for b_block in model.before.b_blocks}

        # register tests
        self.tests = {test.name: test for test in model.tests}

        # register after blocks
        if model.after:
            self.afters = {a_block.name: a_block.a_steps for a_block in model.after.a_blocks}

        # register after all steps
        if model.after_all:
            self.after_alls = model.after_all.aa_steps

    def run_all(self):
        self.setup_testing()

        for test in self.tests.keys():
            self.run_test(test, single=False)

        self.teardown_testing()

    def setup_testing(self):
        self.instantiate_actors()

        self.test_report.clear()
        self.test_report['BA'] = []             # before all errors
        self.test_report['TC'] = 0              # test count
        self.test_report['CT'] = (None, [])     # current test with errors
        self.test_report['ST'] = []             # successful tests
        self.test_report['FT'] = []             # failed tests
        self.test_report['AA'] = []             # after all errors

        if len(self.before_alls) > 0:
            self.print_if_verbose(TText.INFO + 'Running BeforeAll' + TText.ENDC)

        self.add_error_fun = lambda l, e : self.test_report['BA'].append((l, e))
        self.process_steps(self.before_alls, tb_lvl=1)

    def instantiate_actors(self):
        self.print_if_verbose()
        if len(self.actor_definitions) > 0:
            self.print_if_verbose(self.instance_row.format('Instance', 'Class', 'Attributes'))
            self.print_if_verbose(self.instance_row.format('-' * 15, '-' * 15, '-' * 63))
        for actor_name in self.actor_definitions:
            actor = self.actor_definitions[actor_name]
            actor_class = actor[0]
            attributes = actor[1]

            instance = actor_class()
            for attribute in attributes:
                setattr(instance, attribute.name, attribute.value)
            self.actors[actor_name] = instance

            self.print_if_verbose(self.instance_row.format(actor_name, actor_class.__name__, str(instance.__dict__)))
        self.print_if_verbose()

    def teardown_testing(self):
        if len(self.after_alls) > 0:
            self.print_if_verbose(TText.INFO + 'Running AfterAll' + TText.ENDC)

        self.add_error_fun = lambda l, e : self.test_report['AA'].append((l, e))
        self.process_steps(self.after_alls, tb_lvl=1)

        self.actors.clear()

    def run_test(self, test_name, single=True):
        if single:
            self.setup_testing()

        # get test name
        print(TText.INFO + 'Running Test "' + test_name + '"' + TText.ENDC)
        test = self.tests[test_name]
        self.set_current_test(test_name)

        # process all before steps
        self.process_before_after_test('Before', test.befores, self.befores)

        # process test execution steps
        if len(test.e_steps) > 0:
            self.print_if_verbose(TText.INFO + 'Execute Test' + TText.ENDC, tb_lvl=1)
        self.add_error_fun = lambda l, e: self.test_report['CT'][1].append((l, e))
        self.process_steps(test.e_steps, tb_lvl=2)

        # process all after steps
        self.process_before_after_test('After', test.afters, self.afters)

        # update test report
        self.update_test_report()

        if single:
            self.teardown_testing()

    def process_before_after_test(self, type, calls, steps):
        if len(calls) > 0:
            self.print_if_verbose(TText.INFO + 'Running ' + type + TText.ENDC, tb_lvl=1)
        for call in calls:
            self.print_if_verbose(TText.INFO + '"' + call.name + '" OK' + TText.ENDC, tb_lvl=2)
            self.add_error_fun = lambda l, e: self.test_report['CT'][1].append(
                (TText.INFO + 'In ' + type + ' Clause: ' + l, e))
            self.process_steps(steps[call.name], tb_lvl=3)

    def process_steps(self, steps, tb_lvl=0):
        for step in steps:
            self.process_step(step, tb_lvl)

    def process_step(self, step, tb_lvl=0):
        step_type = step.__class__.__name__
        if step_type == 'AssignStep':
            self.process_assign_step(step)
        elif step_type == 'CallStep':
            self.process_call_step(step)
        elif step_type == 'AssertStep':
            self.process_assert_step(step, tb_lvl)
        elif step_type == 'TimeStep':
            time.sleep(step.delay / 1000)

    def process_assign_step(self, step):
        actor, attribute = self.get_attr_ref(step)
        setattr(actor, attribute, step.value)

    def process_call_step(self, step):
        actor = self.actors[step.actor.name]
        method = getattr(actor, step.method)
        args = [p.value if p.actor is None else self.actors[p.actor.name] for p in step.parameters]
        method(*args)

    def process_assert_step(self, step, tb_lvl=0):
        actor_name = step.attributeReference.actor.name
        actor, attribute = self.get_attr_ref(step)
        actual_value = getattr(actor, attribute)
        expected_value = step.value

        if actual_value != expected_value:
            line, column = self.model._tx_parser.pos_to_linecol(step._tx_position)
            line_info = \
                TText.WARN + 'Assertion ' + TText.BOLD + 'ERROR' + TText.ENDC + \
                TText.WARN + ' in ' + TText.UL + 'line {} column {}:'.format(line, column) + TText.ENDC
            error_msg = \
                TestSuite.style_assertion('Expected', 'but was', '!', TText.FAIL) \
                    .format(actor_name, attribute, expected_value, actual_value)
            self.add_error_fun(line_info, error_msg)
            message = line_info + '\n' + error_msg
        else:
            message = \
                TText.OK + 'Assertion OK: ' + TText.ENDC + \
                TestSuite.style_assertion('Expected', 'and was', '.', TText.OK) \
                    .format(actor_name, attribute, expected_value, actual_value)
        self.print_if_verbose(message, tb_lvl=tb_lvl)

    def get_attr_ref(self, step):
        actor = self.actors[step.attributeReference.actor.name]
        attribute = step.attributeReference.attribute.name
        return actor, attribute

    def set_current_test(self, test_name):
        self.test_report['CT'] = (test_name, [])

    def update_test_report(self):
        current_test = self.test_report['CT'][0]
        errors = self.test_report['CT'][1]
        if len(errors) == 0:
            self.test_report['ST'].append(current_test)
        else:
            self.test_report['FT'].append(self.test_report['CT'])
        self.test_report['TC'] += 1
        self.test_report['CT'] = (None, [])

    def print_if_verbose(self, text='', tb_lvl=0):
        if self.verbose:
            print('\t' * tb_lvl + text)

    @staticmethod
    def import_actor(actor_obj):
        package = actor_obj.path.replace('-', '.')
        return __import__(package, fromlist=[actor_obj.class_name])

    @staticmethod
    def style_assertion(prefix, infix, suffix, color):
        return color + prefix + TText.BOLD + ' {}[{}]' + TText.ENDC + \
               color + ' == ' + TText.BOLD + '{} ' + TText.ENDC + \
               color + infix + TText.BOLD + ' {}' + TText.ENDC + \
               color + suffix + TText.ENDC
