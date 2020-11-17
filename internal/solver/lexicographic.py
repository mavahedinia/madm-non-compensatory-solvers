from abc import ABC, abstractmethod

from internal.options import DecisionSet
from internal.solver.base import SolverBase


class LexicographicSolverBase(SolverBase, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._validate()

    def _validate(self):
        assert self.extra_parameters is not None
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

    def _filter(self, decisions, column, impact) -> DecisionSet:
        filtered_decisions = DecisionSet()
        filtered_decisions.attrs = decisions.attrs.copy()
        is_reversed = impact == "+"

        sorted_options = sorted(decisions.options, key=lambda row: row[column], reverse=is_reversed)
        for option in sorted_options:
            if self._should_filter(option, sorted_options[0], column):
                continue
            filtered_decisions.options.append(option)

        return filtered_decisions

    @abstractmethod
    def _should_filter(self, option, best_option, column):
        pass

    def _get_attribute_order_indices(self, attr_ordering):
        ordering_indices = []

        for attr in attr_ordering:
            for i, attr_column in enumerate(self.decisions_set.attrs[1:]):
                if attr != attr_column[0]:
                    continue
                ordering_indices.append(i + 1)

        return ordering_indices


class LexicographicSolver(LexicographicSolverBase):
    def _validate(self):
        assert len(self.extra_parameters) == 1
        super()._validate()

    def _should_filter(self, option, best_option, column):
        return option[column] != best_option[column]


class SemiOrderLexicographicSolver(LexicographicSolverBase):
    def _validate(self):
        assert len(self.extra_parameters) == 2
        super()._validate()
        tolerance = float(self.extra_parameters[1][0])
        assert tolerance >= 0
        assert tolerance <= 100

    def _should_filter(self, option, best_option, column):
        tolerance = float(self.extra_parameters[1][0])
        return abs(100.0 * (option[column] - best_option[column]) / best_option[column]) > tolerance
