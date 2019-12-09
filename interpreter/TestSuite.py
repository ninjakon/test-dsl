from abc import ABC, abstractmethod

from interpreter.TText import TText


class TestSuite(ABC):
    def __init__(self, verbose=False):
        # test suite attributes
        self.verbose = verbose
        self.model = None
        self.test_report = {}
        self.add_error_fun = None

        # test elements
        self.global_actor_definitions = {}
        self.actors = {}
        self.before_all = []
        self.befores = {}
        self.tests = {}
        self.afters = {}
        self.after_all = []

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

        # register actors (only definitions not instances)
        self.set_global_actor_definitions(model)

        # register before all steps
        if model.before_all:
            self.set_before_all(model)

        # register before blocks
        if model.before:
            self.set_befores(model)

        # register tests
        self.set_tests(model)

        # register after blocks
        if model.after:
            self.set_afters(model)

        # register after all steps
        if model.after_all:
            self.set_after_all(model)

    @abstractmethod
    def run_all(self):
        pass

    @abstractmethod
    def run_test(self, test_name, single=True):
        pass

    @abstractmethod
    def set_global_actor_definitions(self, model):
        pass

    @abstractmethod
    def set_before_all(self, model):
        pass

    @abstractmethod
    def set_befores(self, model):
        pass

    @abstractmethod
    def set_tests(self, model):
        pass

    @abstractmethod
    def set_afters(self, model):
        pass

    @abstractmethod
    def set_after_all(self, model):
        pass
