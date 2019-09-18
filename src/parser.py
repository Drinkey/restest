import json
from typing import List, Dict
import pathlib
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
    def __init__(self, test_suite_file=None, env='dev', format='yaml'):
        self._test_description_file = None
        self._test_suite_file = test_suite_file
        self._test_suite_folder = pathlib.Path(test_suite_file).resolve().parent
        if test_suite_file:
            self._test_description_file = yaml2dict(test_suite_file)
        self._env = env
        self.variables = dict()

        self.assertions = self._test_description_file.get('assertions', None)
        self.actions = self._test_description_file.get('actions', None)
        self.includes = self._test_description_file.get('includes', None)

        # update included variables
        if self.includes:
            self.do_includes()
        self._test_suite = self._test_description_file.get('testsuite', None)

        # update test file variables
        self.variables.update(self._test_description_file.get('variables', {}))

        self.description = self._test_suite.get('description', None)
        self.setup = self._test_suite['setup']
        self.teardown = self._test_suite.get('teardown', None)

        # update test suite variables
        self.variables.update(self._test_suite.get('variables', {}))

        self.code = PytestCodeBuilder()

    def make(self):
        self.prepare_testsuite()
        self.collect_testcases()

    def prepare_testsuite(self):
        self.code.add_docstring(self.description)
        self.code.add_from_import('assertions', self.assertions)
        self.code.add_from_import('actions', self.actions)
        
        if self.variables:
            self.code.add_variables(self.variables)

    def collect_testcases(self):
        for testcase in self._test_suite['testcases']:
            t = TestCase(testcase, self.code)
            t.make()

    def __str__(self):
        return f"<testsuite>: {self._test_suite}, <env>: {self._env}"

    def do_includes(self):
        for f in self.includes:
            includ_file = f"{self._test_suite_folder}/{f}"
            # print(includ_file)
            read_content = yaml2dict(includ_file)
            # print(read_content)
            self.variables.update(read_content[self._env]['variables'])

    def do_setup(self, setup):
        pass

    def do_teardown(self, teardown):
        pass
    
    def save(self):
        pytest_source = self._test_suite_file.replace('yaml', 'py').replace('-','_')
        with open(pytest_source, 'wb') as fp:
            fp.write(str(self.code).encode())
        return pytest_source


class TestCase:
    def __init__(self, testcase, code):
        self._tc = testcase
        self.name = self._to_pytest_name()
        self.do = self._tc.get('do')
        self.expect = self._tc.get('expect', None)
        self.variables = self._tc.get('variables', None)

        self.code = code

    def _to_pytest_name(self):
        name = self._tc['name'].lower()
        for sep in [' ', '-', '_']:
            name = name.replace(sep, '_')
        return f"test_{name}"

    def make(self):
        self.code.add_func(self.name, [])
        if self.variables:
            self.code.add_variables(self.variables)
        if not isinstance(self.do, list):
            raise SyntaxError

        for do in self.do:
            _action = do.pop('action', 'request')
            _expects = do.pop('expect', None)
            self.code.add_test_step(_action, (f"{k}={v}" for k,v in do.items()))
            if _expects:
                self.code.add_test_expects(_expects)
        # if self.expect:
        #     self.code.add_for_loop()
        #     self.code.add_test_expects(self.expect)
        self.code.dedent()
        self.code.add_blank_line()
