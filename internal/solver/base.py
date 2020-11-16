from abc import ABC, abstractmethod

from internal.options import DecisionSet


class SolverBase(ABC):
    def __init__(self, decisions_set: DecisionSet, *args, **kwargs):
        self.decisions_set = decisions_set

    @abstractmethod
    def _normalize(self):
        pass

    @abstractmethod
    def solve(self) -> DecisionSet:
        pass
