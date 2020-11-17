import csv
from abc import ABC, abstractmethod

from prettytable import PrettyTable

from internal.options import DecisionSet


class ExporterBase(ABC):
    def __init__(self) -> None:
        pass

    def export(self, decisions: DecisionSet):
        pass


class CLIExporter(ExporterBase):
    def export(self, decisions: DecisionSet):
        table = PrettyTable()
        table.add_row([attribute_name for attribute_name, _ in decisions.attrs])
        table.add_row([impact for _, impact in decisions.attrs])

        for option in decisions.options:
            table.add_row(option)

        print(table.get_string(header=False, border=True))


class CSVExporter(ExporterBase):
    def __init__(self, file_name):
        super().__init__
        self.file_name = file_name

    def export(self, decisions: DecisionSet):
        with open(self.file_name, mode="w") as csv_file:
            decisions_writer = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            decisions_writer.writerow([attribute_name for attribute_name, _ in decisions.attrs])
            decisions_writer.writerow([impact for _, impact in decisions.attrs])

            for option in decisions.options:
                decisions_writer.writerow(option)
