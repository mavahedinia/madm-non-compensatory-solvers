import csv
from abc import ABC, abstractmethod

from internal.options import DecisionSet


class InputLoader(ABC):
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def load(self) -> DecisionSet:
        pass


class CSVInputLoader(InputLoader):
    def __init__(self, file_name: str, *args, **kwargs):
        self.file_name = file_name
        super().__init__(*args, **kwargs)

    def load(self) -> DecisionSet:
        attributes = []
        decisions_set = DecisionSet()
        with open(self.file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_count = 0
            for row in csv_reader:
                if line_count <= 1:
                    attributes.append(row)
                    line_count += 1
                else:
                    decisions_set.options.append(row)
                    line_count += 1
        decisions_set.attrs = list(zip(attributes[0], attributes[1]))
        decisions_set.validate()
        return decisions_set


class CSVExtraInputLoader:
    def __init__(self, file_name: str):
        self.file_name = file_name

    def load(self):
        extra_input = []
        with open(self.file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                extra_input.append(row)

        return extra_input
