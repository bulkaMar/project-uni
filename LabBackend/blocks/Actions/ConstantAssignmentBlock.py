import re
from LabBackend.blocks.Conditions.AbstractBlock import AbstractBlock

class ConstantAssignmentBlock(AbstractBlock):
    def __init__(self, id: int, data: str):
        super().__init__(id, data)
        self.name_block = "const"

    def _is_valid_assignment(self, data: str) -> bool:
        return re.match(r'^([a-zA-Z_]\w*)=(\d+)$', data) is not None

    def execute_with_language(self, programming_language: str, amount_tabs: int):
        if not self._is_valid_assignment(self.data):
            print("Invalid assignment format")
            return

        parts = self.data.split('=')
        variable_name = parts[0].strip()
        value = parts[1].strip()

        print(f'Executing {self.id} "{self.name_block}": {self.data}')
        indent = '\t' * amount_tabs

        if programming_language in ("C", "C++", "C#", "Java"):
            print(f"{indent}int {variable_name} = {value};")
        elif programming_language == "Python":
            print(f"{indent}{variable_name} = {value}")
        else:
            print("Unknown programming language")

        # ✅ передати виконання наступним блокам
        for next_block in self.next:
            if next_block is not None:
                next_block.execute_with_language(programming_language, amount_tabs)
