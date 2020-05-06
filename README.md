# 17480 Final Project
  17-480 Final Project Repository. Building an API over the [truffleHog](https://github.com/dxa4481/truffleHog/) library.

[![Build Status](https://travis-ci.com/cakeid/17480-Final-Project.svg?token=x1jLGpFqhXWPzfonGfC3&branch=master)](https://travis-ci.com/cakeid/17480-Final-Project)

## Setup
* `virtualenv -p python3 venv` if you do not have a venv for the project.
* `source venv/bin/activate` activates the virtual env.
* `pip install -r requirements.txt` installs dependencies required for API, including truffleHog itself.

## Tests
Runs all tests - `python3 -m unittest discover -v`

## Documentation
* `pdoc` is installed when you run `pip install -r requirements-dev.txt`
* Generate docs with `PYTHONPATH=. pdoc trufflehog_api --all-submodules --html --html-dir=docs/ --overwrite && 'cp' -rf docs/trufflehog_api/* docs/ && rm -rf docs/trufflehog_api`

Docs are visible in the `/docs/` folder.

## Requirements
https://github.com/cakeid/17480-Final-Project/wiki/Requirements-Document

## Usage examples
Sample client code being applied to usecases can be found in the `/examples` folder

## API Drafts
TODO - Add sketch here as V1 itself

## Issues list
https://github.com/cakeid/17480-Final-Project/issues

## Rationale
https://github.com/cakeid/17480-Final-Project/wiki/Design-Rationale
