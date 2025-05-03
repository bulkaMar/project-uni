import re

from LabBackend.Utils.Abstract import AbstractBlock

class AssignmentBlock(AbstractBlock):
    def __init__(self, id: int, data: str):
        super().__init__(id, data)
        self.NameBlock = "AssignmentBlock"

    def _is_valid_assignment(self, data: str) -> bool:
        return re.match(r'^([a-zA-Z_]\w*)=([a-zA-Z_]\w*)$', data) is not None

    def execute(self, programming_language: str, amount_tabs: int):
        if not self._is_valid_assignment(self.Data):
            print("Invalid assignment format")
            return

        print(f'Executing {self.Id} "{self.NameBlock}": {self.Data}')
        indent = '\t' * amount_tabs
        variables = self.Data.split('=')

        if len(variables) != 2:
            raise ValueError("Data should be in format 'V1=V2'")

        v1 = variables[0].strip()
        v2 = variables[1].strip()

        code_lines = ""

        if programming_language == "C":
            code_lines += f"{indent}strcpy({v1}, {v2});\n"
        elif programming_language in ("C++", "C#", "Java"):
            code_lines += f"{indent}{v1} = {v2};\n"
        elif programming_language == "Python":
            code_lines += f"{indent}{v1} = {v2}\n"
        else:
            raise NotImplementedError(f"Programming language '{programming_language}' is not supported.")

        print(code_lines)