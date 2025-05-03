import re

from LabBackend.Utils.Abstract import AbstractBlock

class InputBlock(AbstractBlock):
    def __init__(self, id: int, data: str):
        super().__init__(id, data)
        self.NameBlock = "InputBlock"

    def _is_valid_variable_name(self, variable_name: str) -> bool:
        return re.match(r'^[a-zA-Z_]\w*$', variable_name) is not None

    def execute(self, programming_language: str, amount_tabs: int):
        if not self._is_valid_variable_name(self.Data):
            print("Invalid variable name format")
            return

        print(f'Executing {self.Id} "{self.NameBlock}": {self.Data}')
        indent = '\t' * amount_tabs

        if programming_language == "C":
            print(f'{indent}scanf("%d", &{self.Data});')
        elif programming_language == "C++":
            print(f'{indent}cin >> {self.Data};')
        elif programming_language == "C#":
            print(f'{indent}{self.Data} = int.Parse(Console.ReadLine());')
        elif programming_language == "Python":
            print(f'{indent}{self.Data} = int(input())')
        elif programming_language == "Java":
            print(f'{indent}{self.Data} = Integer.parseInt(scan.nextLine());')
        else:
            raise NotImplementedError(f"Programming language '{programming_language}' is not supported.")