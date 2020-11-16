class Options:
    attributes = []
    options = []

    def validate(self):
        rows_len = len(self.attributes)
        for option in self.options:
            if len(option) != rows_len:
                raise ValueError("Invalid input")
