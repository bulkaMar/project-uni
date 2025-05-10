import re
from LabBackend.blocks.Conditions.AbstractBlock import AbstractBlock

class InputBlock(AbstractBlock):
    def __init__(self, id: int, data: str):
        super().__init__(id, data)
        self.name_block = "input"  # 🔁 з малої для get_name_block()

    def _is_valid_variable_name(self, variable_name: str) -> bool:
        return re.match(r'^[a-zA-Z_]\w*$', variable_name) is not None

    def execute_with_language(self, programming_language: str, amount_tabs: int):
        if not self._is_valid_variable_name(self.data):
            print("Invalid variable name format")
            return

        print(f'Executing {self.id} "{self.name_block}": {self.data}')
        indent = '\t' * amount_tabs

        if programming_language == "C":
            print(f'{indent}scanf("%d", &{self.data});')
        elif programming_language == "C++":
            print(f'{indent}cin >> {self.data};')
        elif programming_language == "C#":
            print(f'{indent}{self.data} = int.Parse(Console.ReadLine());')
        elif programming_language == "Python":
            print(f'{indent}{self.data} = int(input())')
        elif programming_language == "Java":
            print(f'{indent}{self.data} = Integer.parseInt(scan.nextLine());')
        else:
            raise NotImplementedError(f"Programming language '{programming_language}' is not supported.")

        # ✅ передати виконання далі
        for next_block in self.next:
            if next_block is not None:
                next_block.execute_with_language(programming_language, amount_tabs)
