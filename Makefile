.PHONY: serve setup clean

VENV := .venv
MKDOCS := $(VENV)/bin/mkdocs
PIP := $(VENV)/bin/pip
STAMP := $(VENV)/.requirements-installed

setup: $(STAMP)

$(STAMP): requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	@touch $(STAMP)

serve: setup
	$(MKDOCS) serve

clean:
	rm -rf $(VENV) site
