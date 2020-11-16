import argparse

from internal.exporter import CLIExporter
from internal.loader import CSVExtraInputLoader, CSVInputLoader
from internal.solver import *

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file-name", help="Input file")
parser.add_argument("-p", "--extra-input", help="Extra Input File")
parser.add_argument("-m", "--method", help="Solving method")


def get_sovler(solver_name) -> SolverBase:
    solvers = {
        "dominance": DominanceSolver,
        "maximin": SolverBase,
        "maximax": SolverBase,
        "conjunctive": SolverBase,
        "disjunctive": SolverBase,
        "lexicographic": LexicographicSolver,
        "lexicographic-semi-order": SolverBase,
        "permutation": SolverBase,
    }

    if solver_name not in solvers:
        raise Exception("Invalid solving method.")

    return solvers[solver_name]


if __name__ == "__main__":
    args = parser.parse_args()
    decisions_set = CSVInputLoader(file_name=args.file_name).load()
    extra_input = CSVExtraInputLoader(file_name=args.extra_input).load() if args.extra_input is not None else None

    solver_class = get_sovler(args.method)
    solver_instance = solver_class(decisions_set=decisions_set, extra_parameters=extra_input)
    best_decisions = solver_instance.solve()

    exporter = CLIExporter
    exporter.export(best_decisions)
