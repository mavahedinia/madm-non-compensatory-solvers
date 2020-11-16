from internal.options import DecisionSet
from internal.solver.base import SolverBase


class LexicographicSolver(SolverBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._validate()

    def _validate(self):
        assert self.extra_parameters is not None
        assert len(self.extra_parameters) == 1
        attr_names = [name for name, _ in self.decisions_set.attrs[1:]]
        attr_ordering_set = set()
        for attr in self.extra_parameters[0]:
            assert attr in attr_names
            attr_ordering_set.add(attr)
        assert len(attr_ordering_set) == len(self.extra_parameters[0])

    def solve(self) -> DecisionSet:
        best_decisions = DecisionSet()
        best_decisions.attrs = self.decisions_set.attrs.copy()
        best_decisions.options = self.decisions_set.options.copy()

        attr_orders = self._get_attribute_order_indices(self.extra_parameters[0])

        for current_column in attr_orders:
            if len(best_decisions.options) == 1:
                break
            best_decisions = self._filter(best_decisions, current_column, best_decisions.attrs[current_column][1])

        return best_decisions

    @staticmethod
    def _filter(decisions, column, impact) -> DecisionSet:
        filtered_decisions = DecisionSet()
        filtered_decisions.attrs = decisions.attrs.copy()
        is_reversed = impact == "+"

        sorted_options = sorted(decisions.options, key=lambda row: row[column], reverse=is_reversed)
        for i, option in enumerate(sorted_options):
            filtered_decisions.options.append(option)
            if (i != len(sorted_options) - 1) and (sorted_options[i + 1][column] != option[column]):
                break

        return filtered_decisions

    def _get_attribute_order_indices(self, attr_ordering):
        ordering_indices = []

        for attr in attr_ordering:
            for i, attr_column in enumerate(self.decisions_set.attrs[1:]):
                if attr != attr_column[0]:
                    continue
                ordering_indices.append(i + 1)

        return ordering_indices
