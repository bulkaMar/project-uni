import re

from LabBackend.Utils.Abstract import AbstractBlock

class PrintBlock(AbstractBlock):
    def __init__(self, id: int, data: str):
        super().__init__(id, data)
        self.NameBlock = "PrintBlock"

    def _is_valid_variable_name(self, variable_name: str) -> bool:
        return re.match(r'^[a-zA-Z_]\w*$', variable_name) is not None

    def execute(self, programming_language: str, amount_tabs: int):
        if not self._is_valid_variable_name(self.Data):
            print("Invalid variable name format")
            return

        print(f'Printing {self.Id} "{self.NameBlock}": {self.Data}')
        indent = '\t' * amount_tabs

        if programming_language == "C":
            print(f'{indent}printf("%s", {self.Data});')
        elif programming_language == "C++":
            print(f'{indent}std::cout << {self.Data} << std::endl;')
        elif programming_language == "C#":
            print(f'{indent}Console.WriteLine({self.Data});')
        elif programming_language == "Python":
            print(f'{indent}print({self.Data})')
        elif programming_language == "Java":
            print(f'{indent}System.out.println({self.Data});')
        else:
            raise NotImplementedError(f"Programming language '{programming_language}' is not supported.")