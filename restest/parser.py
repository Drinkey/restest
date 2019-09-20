import json
import pathlib
from typing import List, Dict
from ruamel.yaml import YAML

from restest.code import CodeBuilder, PytestCodeBuilder

PKG = 'restest'

def yaml2dict(src):
    ret = {}
    yaml = YAML()
    with open(src, 'r') as f:
        ret = yaml.load(f)
    return json.loads(json.dumps(ret))


class ParamError(Exception):
    pass

class TestSuites:
    def __init__(self, test_suite_folder: str, env='qa', filetype: str='yaml',
                 cache_dir: str='sdist'):
        self._test_suite_folder = pathlib.Path(test_suite_folder)
        self._env = env
        self._filetype = filetype
        self._cache_dir = cache_dir

    def _discover(self):
        return sorted(self._test_suite_folder.glob(f'test*.{self._filetype}'))

    def collect(self):
        for _test_suite in self._discover():
            _ts = TestSuite(str(_test_suite), env=self._env, 
                                          filetype=self._filetype, 
                                          cache_dir=self._cache_dir)
            _ts.make()
            _ts.save()
        return self._test_suite_folder / self._cache_dir


class TestSuite:
    def __init__(self, test_suite_file: str, env: str='dev', filetype: str='yaml',
                 cache_dir: str='sdist'):
        self._temp_pytest_output_dir = cache_dir
        self._test_suite_file = pathlib.Path(test_suite_file).resolve()
        self._test_suite_folder = self._test_suite_file.parent
        

        self._testsuite_object = yaml2dict(test_suite_file)

        self._env = env
        self.variables = dict()

        self.assertions = self._testsuite_object.get('assertions', None)
        self.actions = self._testsuite_object.get('actions', None)
        self.includes = self._testsuite_object.get('includes', None)

        # update included variables
        if self.includes:
            self.do_includes()
        self._test_suite = self._testsuite_object.get('testsuite', None)

        # update test file variables
        self.variables.update(self._testsuite_object.get('variables', {}))

        self.description = self._test_suite.get('description', None)
        self.setup = self._test_suite.get('setup', None)
        self.teardown = self._test_suite.get('teardown', None)

        # update test suite variables
        self.variables.update(self._test_suite.get('variables', {}))

        self.code = PytestCodeBuilder()

    def make(self):
        self.prepare_testsuite()
        self.collect_testcases()

    def prepare_testsuite(self):
        self.code.add_docstring(self.description)
        self.code.add_from_import(f'{PKG}.assertions', self.assertions)
        self.code.add_from_import(f'{PKG}.actions', self.actions)
        
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
        """save generate pytest code to a file

        The file folder is at the save level of the yaml file

        For example, if the yaml file is /x/y/z/test_001.yaml, the output pytest file should
        be: /x/y/z/<temp_cache_dir>/test_001.py

        The parameter <temp_cache_dir> can be set by cache_dir.
        
        :return: the file path of generated pytest file
        :rtype: str
        """
        _pytest_filename = self._test_suite_file.name.replace('yaml', 'py').replace('-','_')
        _pytest_folder = self._test_suite_folder / self._temp_pytest_output_dir
        _pytest_folder.mkdir(parents=True, exist_ok=True)
        _pytest_source = _pytest_folder / _pytest_filename

        with _pytest_source.open('wb') as fp:
            fp.write(str(self.code).encode())
        return str(_pytest_source)


class TestCase:
    def __init__(self, testcase: Dict, code: PytestCodeBuilder):
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
