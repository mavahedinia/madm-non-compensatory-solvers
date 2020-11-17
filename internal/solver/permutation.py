from collections import defaultdict
from itertools import permutations

from internal.options import DecisionSet
from internal.solver.base import SolverBase


def default_dict_maker():
    return defaultdict(lambda: 0.0)


class PermutationSolver(SolverBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._validate()
        self.comparison_matrix = self._get_comparison_matrix()

    def _validate(self):
        assert self.extra_parameters is not None
        assert len(self.extra_parameters) == 2
        attr_names = [name for name, _ in self.decisions_set.attrs[1:]]
        attr_set = set()
        for attr in self.extra_parameters[0]:
            assert attr in attr_names
            attr_set.add(attr)
        assert len(attr_set) == len(self.extra_parameters[0])
        assert len(attr_set) == len(self.decisions_set.attrs[1:])
        assert len(self.extra_parameters[1]) == len(self.decisions_set.attrs[1:])
        assert sum([float(w) for w in self.extra_parameters[1]]) >= 1.0 - 1e-6

    def solve(self) -> DecisionSet:
        best_decisions = DecisionSet()
        best_decisions.attrs = self.decisions_set.attrs.copy()

        options_list = self.decisions_set.get_options_list()
        best_permutation_score = -10000000000.0

        for p in permutations(options_list):
            permutation_score = self._calcute_permutation_score(p)
            if permutation_score > best_permutation_score:
                best_permutation_score = permutation_score
                best_decisions.options = self.decisions_set.reorder_options(p)

        return best_decisions

    def _calcute_permutation_score(self, permutation):
        score = 0.0
        for i, option_1 in enumerate(permutation):
            for j, option_2 in enumerate(permutation):
                if j <= i:
                    continue

                score += self.comparison_matrix[option_1][option_2] - self.comparison_matrix[option_2][option_1]

        return score

    def _get_comparison_matrix(self):
        weights = self._get_attributes_weights()
        comparison_matrix = defaultdict(default_dict_maker)
        impacts = self.decisions_set.get_attributes_impact()

        for option_1 in self.decisions_set.options:
            for option_2 in self.decisions_set.options:
                comparison_matrix[option_1[0]][option_2[0]] = sum(
                    [
                        (opt1 >= opt2 if impact == "+" else opt1 <= opt2) * weight
                        for opt1, opt2, impact, weight in zip(option_1[1:], option_2[1:], impacts, weights)
                    ]
                )

        return comparison_matrix

    def _get_attributes_weights(self):
        weights = [0.0] * len(self.extra_parameters[0])
        for attribute_name, weight in zip(self.extra_parameters[0], self.extra_parameters[1]):
            for i, attr in enumerate(self.decisions_set.attrs):
                if attribute_name != attr[0]:
                    continue
                weights[i - 1] = float(weight)

        return weights
