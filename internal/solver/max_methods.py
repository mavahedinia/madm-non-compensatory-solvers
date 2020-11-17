from internal.options import DecisionSet
from internal.solver.base import SolverBase


class MaxSolverBase(SolverBase):
    def _normalize(self):
        self._normalized_decision_set = DecisionSet()
        self._normalized_decision_set.attrs = self.decisions_set.attrs.copy()
        self._normalized_decision_set.options = self.decisions_set.options.copy()

        for i, attr in enumerate(self.decisions_set.attrs):
            if i == 0:
                continue

            column = [option[i] for option in self._normalized_decision_set.options]
            normalized_column = self._normalize_column(column, attr[1])

            for j, normalized_field in enumerate(normalized_column):
                self._normalized_decision_set.options[j][i] = normalized_field

    @staticmethod
    def _normalize_column(column, impact):
        normalized_column = column.copy()
        normalization_factor = max(column) if impact == "+" else min(column)

        for i, value in enumerate(normalized_column):
            normalized_column[i] = value / normalization_factor if impact == "+" else normalization_factor / value

        return normalized_column

    def solve(self) -> DecisionSet:
        self._normalize()

        best_decisions = DecisionSet()
        best_decisions.attrs = self._normalized_decision_set.attrs.copy()

        options = sorted(self._normalized_decision_set.options, key=self._get_row_factor, reverse=True)

        for option in options:
            if self._get_row_factor(option) != self._get_row_factor(options[0]):
                break

            best_decisions.options.append(option)

        return best_decisions

    @staticmethod
    def _get_row_factor(row) -> float:
        return row[0]


class MaxiMinSolver(MaxSolverBase):
    @staticmethod
    def _get_row_factor(row) -> float:
        return min(row[1:])


class MaxiMaxSolver(MaxSolverBase):
    @staticmethod
    def _get_row_factor(row) -> float:
        return max(row[1:])
