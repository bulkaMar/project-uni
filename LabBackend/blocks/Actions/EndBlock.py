from LabBackend.blocks.Conditions.AbstractBlock import AbstractBlock

class EndBlock(AbstractBlock):
    def __init__(self, id: int):
        super().__init__(id, "")
        self.name_block = "end"  # 🔁 з малої літери

    def execute(self):
        print("End block executed")  # 🔁 виправлено текст

    def execute_with_language(self, programming_language: str, amount_tabs: int):
        indent = '\t' * amount_tabs
        if programming_language in ("Python", "C", "C++", "Java", "C#"):
            print(f"{indent}// end")  # або просто закоментований кінець
        else:
            print(f"{indent}// Unknown language end block")
