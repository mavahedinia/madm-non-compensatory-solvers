import argparse

from internal.exporter import CLIExporter, CSVExporter
from internal.loader import CSVExtraInputLoader, CSVInputLoader
from internal.solver import *

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file-name", help="Input file", required=True)
parser.add_argument("-m", "--method", help="Solving method", required=True)
parser.add_argument("-p", "--extra-input", help="Extra Input File (Parameters)")
parser.add_argument("-o", "--output", help="Output File Path")


def get_sovler(solver_name) -> SolverBase:
    solvers = {
        "dominance": DominanceSolver,
        "maximin": MaxiMinSolver,
        "maximax": MaxiMaxSolver,
        "conjunctive": ConjunctiveSolver,
        "disjunctive": DisjunctiveSolver,
        "lexicographic": LexicographicSolver,
        "lexicographic-semi-order": SemiOrderLexicographicSolver,
        "permutation": PermutationSolver,
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

    if args.output is not None:
        exporter = CSVExporter(file_name=args.output)
    else:
        exporter = CLIExporter()

    exporter.export(best_decisions)
