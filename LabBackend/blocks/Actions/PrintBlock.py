import re
from LabBackend.blocks.Conditions.AbstractBlock import AbstractBlock

class PrintBlock(AbstractBlock):
    def __init__(self, id: int, data: str):
        super().__init__(id, data)
        self.name_block = "print"

    def _is_valid_variable_name(self, variable_name: str) -> bool:
        return re.match(r'^[a-zA-Z_]\w*$', variable_name) is not None

    def execute_with_language(self, programming_language: str, amount_tabs: int):
        if not self._is_valid_variable_name(self.data):
            print("Invalid variable name format")
            return

        print(f'Printing {self.id} "{self.name_block}": {self.data}')
        indent = '\t' * amount_tabs

        if programming_language == "C":
            print(f'{indent}printf("%s", {self.data});')
        elif programming_language == "C++":
            print(f'{indent}std::cout << {self.data} << std::endl;')
        elif programming_language == "C#":
            print(f'{indent}Console.WriteLine({self.data});')
        elif programming_language == "Python":
            print(f'{indent}print({self.data})')
        elif programming_language == "Java":
            print(f'{indent}System.out.println({self.data});')
        else:
            raise NotImplementedError(f"Programming language '{programming_language}' is not supported.")

        # ✅ Переходимо до наступних блоків
        for next_block in self.next:
            if next_block:
                next_block.execute_with_language(programming_language, amount_tabs)
