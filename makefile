.PHONY: help clean build install

help:
	@cat makefile

clean:
	@rm -fr venv build dist *.egg-info
	@find . -depth -type d -name __pycache__ -exec rm -fr {} \;

venv:
	@python3 -m venv venv
	@venv/bin/python -m pip install --upgrade pip setuptools wheel build -r requirements.txt

build: venv
	@rm -fr build dist *.egg-info
	@venv/bin/python -m build

install: venv
	@venv/bin/pip install --upgrade .
