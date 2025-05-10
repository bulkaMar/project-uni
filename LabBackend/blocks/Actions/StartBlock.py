from LabBackend.blocks.Conditions.AbstractBlock import AbstractBlock

class StartBlock(AbstractBlock):
    def __init__(self, id):
        super().__init__(id, "")
        self.name_block = "start"

    def execute(self):
        print("Start block executed")
        super().execute()

    def execute_with_language(self, programming_language: str, amount_tabs: int):
        print("Start block executed in language mode")
        for next_block in self.next:
            if next_block:
                next_block.execute_with_language(programming_language, amount_tabs)
