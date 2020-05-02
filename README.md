# 17480 Final Project
  17-480 Final Project Repository. Building an API over the [truffleHog](https://github.com/dxa4481/truffleHog/) library.

[![Build Status](https://travis-ci.com/cakeid/17480-Final-Project.svg?token=x1jLGpFqhXWPzfonGfC3&branch=master)](https://travis-ci.com/cakeid/17480-Final-Project)

## Folder structure

Ken Reitz's python repository structure recommendation ([Link](https://www.kennethreitz.org/essays/repository-structure-and-python))

## Setup
* `virtualenv -p python3 venv` if you do not have a venv for the project.
* `source venv/bin/activate` activates the virtual env.
* `pip install -r requirements.txt` installs dependencies required for API, including truffleHog itself.

## Tests
`python3 -m unittest discover -v`

## Requirements

* As a security engineer, I want to use the trufflehog library API in my security webservice to find secrets in my repositories.
* As a security engineer, I want to find secrets only in a subset of my repositories, some of which are private for a security audit of the company.
* As a security engineer, I want the results of these finding summarized and dumped somewhere so I can alert corresponding stakeholders via a webhook or alert

More information can be found on the wiki page:  
https://github.com/cakeid/17480-Final-Project/wiki/Requirements-Document

## API Sketch
* [v0.1](https://github.com/cakeid/17480-Final-Project/tree/41e253e29f05c0b3c0132ae903e83078cc1885b8/api/name_pending)

## Applying to usecases
Sample client code with skeleton

## API Final Draft
Link to folder

## Documentation
Will this be separate?

## Issues list
https://github.com/cakeid/17480-Final-Project/issues

## Rationale
https://github.com/cakeid/17480-Final-Project/wiki/Design-Rationale
