from internal.options import DecisionSet
from internal.solver.base import SolverBase


class DominanceSolver(SolverBase):
    @staticmethod
    def is_dominant(dominant_option, dominated_option, attribute_types):
        return all(
            [
                dominant_attribute >= dominated_attribute if attribute_type is "+" else dominant_attribute <= dominated_attribute
                for dominant_attribute, dominated_attribute, attribute_type in zip(
                    dominant_option[1:], dominated_option[1:], attribute_types[1:]
                )
            ]
        )

    def option_is_dominated(self, option):
        for dominant_option in self.decisions_set.options:
            if dominant_option[0] == option[0]:
                continue
            if self.is_dominant(dominant_option, option, self.decisions_set.get_attributes_impact()):
                return True

        return False

    def solve(self) -> DecisionSet:
        best_decisions = DecisionSet()
        best_decisions.attrs = list(self.decisions_set.attrs)

        for option in self.decisions_set.options:
            if self.option_is_dominated(option):
                continue
            best_decisions.options.append(list(option))

        return best_decisions
