from typing import Dict, Iterable, List

INDENT_STEP = 4

class CodeBuilder:
    """Generate Python code
    """
    def __init__(self, indent: int=0) -> None:
        self.code = []
        self._indent_level = indent

    def indent(self) -> None:
        """ Increase the indent level """
        self._indent_level += INDENT_STEP

    def dedent(self) -> None:
        """ Decrease the indent level """
        self._indent_level -= INDENT_STEP

    def __str__(self) -> str:
        return "".join(str(s) for s in self.code)

    def add_line(self, line: str) -> None:
        """ add one line of code with indentation"""
        self.code.extend([" " * self._indent_level, line, "\n"])

    def add_blank_line(self) -> None:
        self.code.append('\n')

class PythonCodeBuilder(CodeBuilder):
    def __init__(self, indent: int=0):
        CodeBuilder.__init__(self, indent)

    def add_docstring(self, string: str) -> None:
        self.add_line(f'"""{string}\n"""')

    def add_func(self, name: str, params: Iterable) -> None:
        self.add_line(f'def {name}({", ".join(params)}):')
        self.indent()

    def add_import(self, imports: Iterable) -> None:
        for imp in imports:
            self.add_line(f"import {imp}")

    def add_from_import(self, pkg: str, modules: Iterable) -> None:
        self.add_line(f"from {pkg} import {', '.join(modules)}")
        self.add_blank_line()

    def add_for_loop(self, each: str, iterobject: str) -> None:
        self.add_line(f"for {each} in {iterobject}:")
        self.indent()

    def add_variables(self, variables: Dict) -> None:
        for k,v in variables.items():
            if '{' in v and '}' in v:
                self.add_line(f"{k} = f{repr(v)}")
            else:
                self.add_line(f"{k} = {repr(v)}")
        self.add_blank_line()
    
class PytestCodeBuilder(PythonCodeBuilder):
    def __init__(self, indent: int=0):
        PythonCodeBuilder.__init__(self, indent)

    def add_test_step(self, func_name: str, param: List) -> None:
        self.add_line(f"responses = {func_name}({', '.join(param)})")

    def add_test_expects(self, expects: Iterable) -> None:
        self.add_for_loop('response', 'responses')
        for assert_stmt in expects:
            if isinstance(assert_stmt, dict):
                for k,v in assert_stmt.items():
                    self.add_line(f"{k}(response, {v})")
            else:
                self.add_line(f"{assert_stmt}(response)")
        self.dedent()
        self.dedent()