SHELL := /bin/bash
USER_FLAG := $(shell [[ -z $$VIRTUAL_ENV ]] && echo '--user')
.DEFAULT_GOAL := test
FORCE:

init:
	pip install $(USER_FLAG) -r requirements.txt

init-dev:	init
	pip install $(USER_FLAG) -r requirements-dev.txt

analyze:
	flake8 file_processing_pipeline
	pylint file_processing_pipeline

test: export PYTHONDONTWRITEBYTECODE = 1
test: FORCE analyze
	rm -rf ./test/resources/output_root/
	python -m pytest -x -s -p no:cacheprovider --cov-report term-missing --cov=file_processing_pipeline test --cov-fail-under=100 --basetemp=./tmp/

build: FORCE
	python setup.py bdist_wheel

install: build
	pip install $(USER_FLAG) --upgrade --force-reinstall dist/file_processing_pipeline-1.0.0-py3-none-any.whl

uninstall:
	pip uninstall $(USER_FLAG) -y file_processing_pipeline

clean:
	rm -rf ./build/
	rm -rf ./file_processing_pipeline.egg-info/
	rm -rf ./dist/
	rm -rf ./test/resources/output_root/

diagram:
	pyreverse -o png file_processing_pipeline
	rm classes.png
	mv packages.png docs/
