class DecisionSet:
    def __init__(self):
        self.attrs = []
        self.options = []

    def get_attributes_impact(self):
        return [impact for _, impact in self.attrs]

    def get_options_list(self):
        return [option[0] for option in self.options]

    def reorder_options(self, options_names):
        options = []
        for option_name in options_names:
            for option in self.options:
                if option[0] != option_name:
                    continue
                options.append(option)

        return options

    def validate(self):
        rows_len = len(self.attrs)
        for i, option in enumerate(self.options):
            if len(option) != rows_len:
                raise ValueError("Invalid input")
            for j in range(1, len(option)):
                self.options[i][j] = float(self.options[i][j])
