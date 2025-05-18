from LabBackend.blocks.Conditions.AbstractBlock import AbstractBlock

class EndBlock(AbstractBlock):
    def __init__(self, id: int):
        super().__init__(id, "")
        self.name_block = "end"

    def execute(self):
        print("End block executed")

    def execute_with_language(self, programming_language: str, amount_tabs: int):
        indent = '\t' * amount_tabs
        if programming_language in ("Python", "C", "C++", "Java", "C#"):
            print(f"{indent}// end")
        else:
            print(f"{indent}// Unknown language end block")
