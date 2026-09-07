PYTHON = python3
SRC = a_maze_ing.py
CONFIG = config.txt

all: run

run:
	$(PYTHON) $(SRC) $(CONFIG)

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 .
	mypy --strict .

clean:
	rm -rf __pycache__ */__pycache__
	rm -rf .mypy_cache */.mypy_cache
	rm -rf .pytest_cache
	rm -rf build dist *.egg-info

.PHONY: all run lint lint-strict clean