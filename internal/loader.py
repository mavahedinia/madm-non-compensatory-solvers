import csv
from abc import ABC, abstractmethod

from internal.options import Options


class InputLoader(ABC):
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def load(self) -> Options:
        pass


class CSVInputLoader(InputLoader):
    def __init__(self, file_name: str, *args, **kwargs):
        self.file_name = file_name
        super().__init__(*args, **kwargs)

    def load(self) -> Options:
        attributes = []
        options = Options()
        with open(self.file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_count = 0
            for row in csv_reader:
                if line_count <= 1:
                    attributes.append(row)
                    line_count += 1
                else:
                    options.options.append(row)
                    line_count += 1
        options.attributes = list(zip(attributes[0], attributes[1]))
        return options
