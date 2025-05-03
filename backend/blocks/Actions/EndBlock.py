from LabBackend.Utils.Abstract import AbstractBlock

class EndBlock(AbstractBlock):
    def __init__(self, id: int):
        super().__init__(id, "")
        self.NameBlock = "end"

    def execute(self):
        print("Start block executed")