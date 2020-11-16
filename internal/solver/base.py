from abc import ABC, abstractmethod

from internal.options import DecisionSet


class SolverBase(ABC):
    def __init__(self, decisions_set: DecisionSet, extra_parameters=None):
        self.decisions_set = decisions_set
        self.extra_parameters = extra_parameters

    @abstractmethod
    def solve(self) -> DecisionSet:
        pass
