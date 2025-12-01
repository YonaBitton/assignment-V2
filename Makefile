#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = assignment-levontin
PYTHON_VERSION = 3.10

#################################################################################
# Setup Commands                                                                #
#################################################################################

.PHONY: download-poetry
## Download poetry
download-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

.PHONY: install
## Install Python dependencies using poetry
install:
	@poetry env use $(PYTHON_VERSION)
	@poetry lock -n
	@poetry install -n
	@poetry run pre-commit install -t pre-commit -t pre-push

.PHONY: format-code
## Format & lint code using pre-commit (ruff, nbstripout, codespell, sqlfluff, etc.)
format-code:
	@poetry run pre-commit run --all-files

#################################################################################
# Test Commands                                                                 #
#################################################################################

.PHONY: test
## Run tests using pytest
test:
	@poetry run pytest -vv --cov=lib --cov-report=term-missing tests/

#################################################################################
# Utility Commands                                                              #
#################################################################################

.PHONY: run-streamlit
## Run the Streamlit app
run-streamlit:
	@poetry run streamlit run lib/app.py

.PHONY: run-mkdocs
## Run mkdocs server (if you add docs later)
run-mkdocs:
	@poetry run mkdocs serve
