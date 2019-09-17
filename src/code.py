from typing import Tuple, List

INDENT_STEP = 4

class CodeBuilder:
    """Generate Python code
    """
    def __init__(self, indent=0):
        self.code = []
        self._indent_level = indent

    def indent(self):
        """ Increase the indent level """
        self._indent_level += INDENT_STEP

    def dedent(self):
        """ Decrease the indent level """
        self._indent_level -= INDENT_STEP

    def __str__(self):
        return "".join(str(s) for s in self.code)

    def add_docstring(self, string):
        self.add_line(f'"""{string}\n"""')

    def add_line(self, line):
        """ add one line of code with indentation"""
        self.code.extend([" " * self._indent_level, line, "\n"])
    
    def add_blank_line(self):
        self.code.append('\n')


class PytestCodeBuilder(CodeBuilder):
    def __init__(self, indent=0):
        CodeBuilder.__init__(self, indent)
        
    def add_func(self, name, params):
        self.add_line(f'def {name}({",".join(params)}):')
        self.indent()
    
    def add_import(self, imports):
        for imp in imports:
            self.add_line(f"import {imp}")
    
    def add_from_import(self, pkg, modules):
        self.add_line(f"from {pkg} import {', '.join(modules)}")
        self.add_blank_line()

    def add_for_loop(self, each, iterobject):
        self.add_line(f"for {each} in {iterobject}:")
        self.indent()

    def add_action(self, func_name: str, param: List):
        self.add_line(f"responses = {func_name}({','.join(param)})")

    def add_expects(self):
        self.add_for_loop('response', 'responses')
