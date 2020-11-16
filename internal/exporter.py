from abc import ABC, abstractstaticmethod

from prettytable import PrettyTable

from internal.options import DecisionSet


class ExporterBase(ABC):
    def __init__(self) -> None:
        pass

    @abstractstaticmethod
    def export(decisions: DecisionSet):
        pass


class CLIExporter(ExporterBase):
    @staticmethod
    def export(decisions: DecisionSet):
        table = PrettyTable()
        table.add_row([attribute_name for attribute_name, _ in decisions.attrs])
        table.add_row([impact for _, impact in decisions.attrs])

        for option in decisions.options:
            table.add_row(option)

        print(table.get_string(header=False, border=True))
