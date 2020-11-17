class DecisionSet:
    def __init__(self):
        self.attrs = []
        self.options = []

    def get_attributes_impact(self):
        return [impact for _, impact in self.attrs]

    def validate(self):
        rows_len = len(self.attrs)
        for i, option in enumerate(self.options):
            if len(option) != rows_len:
                raise ValueError("Invalid input")
            for j in range(1, len(option)):
                self.options[i][j] = float(self.options[i][j])
