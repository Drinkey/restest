import json
from typing import List, Dict
from ruamel.yaml import YAML
from code import PytestCodeBuilder


def yaml2dict(src):
    ret = {}
    yaml = YAML()
    with open(src, 'r') as f:
        ret = yaml.load(f)
    return json.loads(json.dumps(ret))


class ParamError(Exception):
    pass

class TestSuites:
    def __init__(self, test_suite_folder, env='qa'):
        self._test_suites = self.discover(test_suite_folder)

        if test_suite_folder:
            self._test_suite_files = self.discover(test_suite_folder)
        self.testsuites = [TestSuite(test_suite_file=each_file) for each_file in self._test_suite_files]

    def discover(self, folder) -> List:
        return list()

class TestSuite:
    def __init__(self, test_suite_file=None, env='qa', format='yaml'):
        self._test_description_file = None
        if test_suite_file:
            self._test_description_file = yaml2dict(test_suite_file)
        self._env = env

        self.assertion = self._test_description_file['assertion']
        self.includes = self._test_description_file['includes']
        self._test_suite = self._test_description_file['testsuite']

        self.description = self._test_suite['description']
        self.setup = self._test_suite['setup']
        self.teardown = self._test_suite['teardown']
        self.variables = self._test_suite['variables']
        
        self.code = PytestCodeBuilder()

        self.testcases = list()
        self.add_description()
        self.add_assertion_functions()
        for t in self._test_suite['testcases']:
            _tc = TestCase(t, self.code)
            _tc.make()
            self.testcases.append(_tc)
        # print(self.code)

    def __str__(self):
        return f"<testsuite>: {self._test_suite}, <env>: {self._env}, <testcases>: {self.testcases}"

    def do_includes(self, filename):
        pass

    def add_description(self):
        self.code.add_docstring(self.description)
    
    def add_assertion_functions(self):
        self.code.add_from_import('assertion', self.assertion)

    def do_setup(self, setup):
        pass

    def do_teardown(self, teardown):
        pass

    def collect(self):
        for testcase in self._test_suite['testcases']:
            t = TestCase(testcase, self.code)
            t.make()
            print(self.code)
            self.testcases.append(t)
            print(self.testcases)


class TestCase:
    def __init__(self, testcase, code):
        self._tc = testcase
        self.name = self._to_pytest_name()
        self.action = self._tc['request']
        self.expect = self._tc['expect']
        self._code = code

    def _to_pytest_name(self):
        name = self._tc['name'].lower()
        for sep in [' ', '-', '_']:
            name = name.replace(sep, '_')
        return f"test_{name}"
    
    def make(self):
        self._code.add_func(self.name, [])
        self._code.add_action('do_send', [self.action['method'], 'url',self.action['data']])
        self._code.add_expects()
        for assert_stmt in self.expect:
            if isinstance(assert_stmt, dict):
                for k,v in assert_stmt.items():
                    self._code.add_line(f"{k}(response, {v})")
            else:
                self._code.add_line(f"{assert_stmt}(response)")
        self._code.dedent()
        self._code.dedent()
        self._code.add_blank_line()
