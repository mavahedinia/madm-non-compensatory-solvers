# madm-non-compensatory-solvers

Multi Attribute Decision Making project: Solving a sample problem using non-compensatory methods taught in the class.

# Methods implemented:
* Dominance

* Maximin

* Maximax

* Conjunctive

* Disjunctive

* Lexicography

* Lexicography Semi Order

* Permutation

# How to run
First of all, you need [pypoetry](https://python-poetry.org/) to install project dependencies (also you can simply use `pip` and the `requirements.txt` provided file; however, it is recomended to use pypoetry)

after installing dependencies using `poetry install` you can use the `run.py` to start the project:
```bash
run -m {METHOD} -f {DECISION_SET_CSV_FILE} -p {PROBLEM_PARAMETERS_CSV_FILE} -o {OUTPUT_CSV_FILE}
```

For more information, please check `run.py`