pip=env/bin/python -m pip
python=env/bin/python3
speechsyn=env/bin/speechsyn
poetry=$(python) -m poetry

lint: build
	@$(poetry) check
	@flake8

build:
	# make python environment
	@rm -rf env
	@python -m venv env
	# install poetry (python package builder)
	@$(python) -m pip install poetry
	# update db or csv
	# @sh upload_data.sh
	@$(poetry) build

install: build
	# horse_ai package installation from wheel
	$(pip) install dist/speechsyn*.whl

test: install
	# $(python) tests/test.py

run: test
	@$(python) speechsyn/synthesize.py

.PHONY: lint test build install run

