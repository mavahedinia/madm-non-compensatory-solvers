class DecisionSet:
    def __init__(self):
        self.attrs = []
        self.options = []

    def validate(self):
        rows_len = len(self.attrs)
        for option in self.options:
            if len(option) != rows_len:
                raise ValueError("Invalid input")
