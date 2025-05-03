import re

from LabBackend.Utils.Abstract import AbstractBlock

class ConstantAssignmentBlock(AbstractBlock):
    def __init__(self, id: int, data: str):
        super().__init__(id, data)
        self.NameBlock = "ConstantAssignmentBlock"

    def _is_valid_assignment(self, data: str) -> bool:
        return re.match(r'^([a-zA-Z_]\w*)=(\d+)$', data) is not None

    def execute(self, programming_language: str, amount_tabs: int):
        if not self._is_valid_assignment(self.Data):
            print("Invalid assignment format")
            return

        parts = self.Data.split('=')
        variable_name = parts[0].strip()
        value = parts[1].strip()

        print(f'Executing {self.Id} "{self.NameBlock}": {self.Data}')
        indent = '\t' * amount_tabs

        if programming_language in ("C", "C++", "C#", "Java"):
            print(f"{indent}int {variable_name} = {value};")
        elif programming_language == "Python":
            print(f"{indent}{variable_name} = {value}")
        else:
            print("Unknown programming language")