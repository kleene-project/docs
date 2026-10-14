.PHONY: serve setup check clean

VENV := .venv
MKDOCS := $(VENV)/bin/mkdocs
PIP := $(VENV)/bin/pip
PYTHON := $(VENV)/bin/python
CODESPELL := $(VENV)/bin/codespell
STAMP := $(VENV)/.requirements-installed
STAMP_DEV := $(VENV)/.requirements-dev-installed

setup: $(STAMP)

$(STAMP): requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	@touch $(STAMP)

$(STAMP_DEV): $(STAMP) requirements-dev.txt
	$(PIP) install -r requirements-dev.txt
	@touch $(STAMP_DEV)

serve: setup
	$(MKDOCS) serve

check: $(STAMP) $(STAMP_DEV)
	$(PYTHON) scripts/check_terms.py
	$(PYTHON) scripts/check_frontmatter.py
	$(CODESPELL)
	$(MKDOCS) build --strict

clean:
	rm -rf $(VENV) site
