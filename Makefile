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
	$(PYTHON) -m flake8 . --exclude=.venv
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude=.venv


lint-strict:
	$(PYTHON) -m flake8 . --exclude=.venv
	$(PYTHON) -m mypy . --strict --exclude=.venv


clean:
	rm -rf __pycache__ */__pycache__
	rm -rf .mypy_cache */.mypy_cache
	rm -rf build dist *.egg-info


.PHONY: all run install build lint lint-strict clean
