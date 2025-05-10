import re
from LabBackend.blocks.Conditions.AbstractBlock import AbstractBlock

class AssignmentBlock(AbstractBlock):
    def __init__(self, id: int, data: str):
        super().__init__(id, data)
        self.name_block = "assign"

    def _is_valid_assignment(self, data: str) -> bool:
        return re.match(r'^([a-zA-Z_]\w*)=([a-zA-Z_]\w*)$', data) is not None

    def execute_with_language(self, programming_language: str, amount_tabs: int):
        if not self._is_valid_assignment(self.data):
            print("Invalid assignment format")
            return

        print(f'Executing {self.id} "{self.name_block}": {self.data}')
        indent = '\t' * amount_tabs
        variables = self.data.split('=')

        if len(variables) != 2:
            raise ValueError("Data should be in format 'V1=V2'")

        v1 = variables[0].strip()
        v2 = variables[1].strip()

        if programming_language == "C":
            print(f"{indent}strcpy({v1}, {v2});")
        elif programming_language in ("C++", "C#", "Java"):
            print(f"{indent}{v1} = {v2};")
        elif programming_language == "Python":
            print(f"{indent}{v1} = {v2}")
        else:
            raise NotImplementedError(f"Programming language '{programming_language}' is not supported.")

        for next_block in self.next:
            if next_block is not None:
                next_block.execute_with_language(programming_language, amount_tabs)
