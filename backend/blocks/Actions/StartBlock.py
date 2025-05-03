from LabBackend.Utils.Abstract import AbstractBlock

class StartBlock(AbstractBlock):
    def __init__(self, id):
        super().__init__(id, "")
        self.NameBlock = "start"

    def execute(self):
        print("Start block executed")
        super().execute()