class AbstractBlock:
    def __init__(self, id=None, data=None, ui_array=None):
        if ui_array is not None:
            self.id = 0  # В оригинале было закомментировано generateID()
            self.next = list(ui_array)  # Копируем список
        else:
            self.id = id
            self.data = data
            self.next = []  # пустой список по умолчанию

        self.name_block = None

    def clone(self):
        import copy
        return copy.copy(self)  # поверхностное копирование, как MemberwiseClone

    def get_name_block(self):
        return self.name_block

    def get_id(self):
        return self.id

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def execute(self):
        print(f"Executing AbstractBlock: {self.name_block}, Data: {self.data}\n")
        for next_block in self.next:
            if next_block is not None:
                next_block.execute()

    def execute_with_language(self, programming_language, amount_tabs):
        print(f"Executing AbstractBlock: {self.name_block}, Data: {self.data}\n")
        for next_block in self.next:
            if next_block is not None:
                next_block.execute_with_language(programming_language, amount_tabs)
