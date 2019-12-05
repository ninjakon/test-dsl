from abc import ABC, abstractmethod

from interpreter.TText import TText


class TestSuite(ABC):
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
            # load actor definition from module
            self.set_actor_definition(actor)

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

    @abstractmethod
    def run_all(self):
        pass

    @abstractmethod
    def run_test(self, test_name, single=True):
        pass

    def print_if_verbose(self, text='', tb_lvl=0):
        if self.verbose:
            print('\t' * tb_lvl + text)

    @abstractmethod
    def set_actor_definition(self, actor):
        pass

    @staticmethod
    def style_assertion(prefix, infix, suffix, color):
        return color + prefix + TText.BOLD + ' {}[{}]' + TText.ENDC + \
               color + ' == ' + TText.BOLD + '{} ' + TText.ENDC + \
               color + infix + TText.BOLD + ' {}' + TText.ENDC + \
               color + suffix + TText.ENDC
