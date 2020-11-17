from abc import ABC, abstractmethod

from internal.options import DecisionSet
from internal.solver.base import SolverBase


class StandardLevelSolverBase(SolverBase, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._validate()

    def _validate(self):
        assert self.extra_parameters is not None
        assert len(self.extra_parameters) == 2
        assert len(self.extra_parameters[0]) == len(self.decisions_set.attrs) - 1
        assert len(self.extra_parameters[1]) == len(self.decisions_set.attrs) - 1

        attr_names = [name for name, _ in self.decisions_set.attrs[1:]]
        attr_set = set()
        for attr, req in zip(self.extra_parameters[0], self.extra_parameters[1]):
            assert attr in attr_names
            float(req)
            attr_set.add(attr)
        assert len(attr_set) == len(self.extra_parameters[0])

    def solve(self):
        best_decisions = DecisionSet()
        best_decisions.attrs = self.decisions_set.attrs.copy()

        for option in self.decisions_set.options:
            if self._should_filter(option[1:]):
                continue
            best_decisions.options.append(option)

        return best_decisions

    @abstractmethod
    def _should_filter(self, option):
        pass

    def _get_min_requirements(self):
        min_requirements = [0.0] * (len(self.decisions_set.attrs) - 1)
        for attribute, requirement in zip(self.extra_parameters[0], self.extra_parameters[1]):
            for i, column in enumerate(self.decisions_set.attrs):
                if attribute != column[0]:
                    continue

                min_requirements[i - 1] = float(requirement)
        return min_requirements


class ConjunctiveSolver(StandardLevelSolverBase):
    def _should_filter(self, option):
        min_requirements = self._get_min_requirements()
        impacts = self.decisions_set.get_attributes_impact()[1:]

        return not all(
            [
                attribute >= min_requirement if impact is "+" else attribute <= min_requirement
                for attribute, min_requirement, impact in zip(option, min_requirements, impacts)
            ]
        )


class DisjunctiveSolver(StandardLevelSolverBase):
    def _should_filter(self, option):
        min_requirements = self._get_min_requirements()
        impacts = self.decisions_set.get_attributes_impact()[1:]

        return not any(
            [
                attribute >= min_requirement if impact is "+" else attribute <= min_requirement
                for attribute, min_requirement, impact in zip(option, min_requirements, impacts)
            ]
        )
