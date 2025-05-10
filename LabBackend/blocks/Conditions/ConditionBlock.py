import re
from AbstractBlock import AbstractBlock

class ConditionBlock(AbstractBlock):
    def __init__(self, id, data):
        super().__init__(id=id, data=data)
        self.name_block = "Condition"

    def _is_valid_condition(self, data):
        return re.match(r"^[a-zA-Z_]\w*(==|<)\d+$", data) is not None

    def execute_with_language(self, programming_language, amount_tabs):
        if not self._is_valid_condition(self.data):
            print("Invalid condition format")
            return

        print(f"Executing {self.id} \"{self.name_block}\": {self.data}")

        condition = ""

        if programming_language == "Python":
            condition = "\t" * amount_tabs + f"if {self.data}:"
        elif programming_language in ["C", "C++", "C#", "Java"]:
            condition = "\t" * amount_tabs + f"if ({self.data}) {{"
        else:
            print("Unknown programming language")
            return

        print(condition)
