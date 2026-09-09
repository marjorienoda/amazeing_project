PYTHON = .venv/bin/python
SRC = a_maze_ing.py
CONFIG = config.txt
REQUIREMENTS = requirements.txt


all: run


run:
	$(PYTHON) $(SRC) $(CONFIG)


debug:
	$(PYTHON) -m pdb $(SRC) $(CONFIG)



install:
	python3 -m venv .venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r $(REQUIREMENTS)


build:
	$(PYTHON) -m build


lint:
	flake8 . --exclude=.venv
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


lint-strict:
	flake8 .
	mypy --strict .


clean:
	rm -rf __pycache__ */__pycache__
	rm -rf .mypy_cache */.mypy_cache
	rm -rf build dist *.egg-info


.PHONY: all run install build lint lint-strict clean