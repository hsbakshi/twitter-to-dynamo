SHELL := /bin/bash
PY_VERSION := 3.6

export PYTHONUNBUFFERED := 1

export AWS_PROFILE := default
STACK_NAME := stack-twitter-dynamodb

BASE := $(shell /bin/pwd)
VENV_DIR := $(BASE)/.venv
export PATH := var:$(PATH):$(VENV_DIR)/bin

PYTHON := $(shell /usr/bin/which python$(PY_VERSION))
VIRTUALENV := $(PYTHON) -m venv
ZIP_FILE := $(BASE)/bundle.zip
S3_BUCKET ?= twitter-to-dynamodb

.DEFAULT_GOAL := build
.PHONY: build clean release describe deploy package bundle bundle.local


build:
	$(VIRTUALENV) "$(VENV_DIR)"
	"$(VENV_DIR)/bin/pip$(PY_VERSION)" \
		--isolated \
		--disable-pip-version-check \
		install -Ur requirements.txt

bundle.local:
	zip -r -9 "$(ZIP_FILE)" src
	cd "$(VENV_DIR)/lib/python$(PY_VERSION)/site-packages" \
		&& zip -r9 "$(ZIP_FILE)" *
	cd "$(VENV_DIR)/lib64/python$(PY_VERSION)/site-packages" \
		&& zip -r9 "$(ZIP_FILE)" *

bundle:
	docker run -v $$PWD:/var/task -it lambci/lambda:build-python3.6 /bin/bash -c 'make clean build bundle.local'

package:
	sam package \
		--template-file template.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix sources \
		--output-template-file packaged.yaml

deploy:
	sam deploy \
		--template-file packaged.yaml \
		--stack-name $(STACK_NAME) \
		--capabilities CAPABILITY_IAM \
		--region us-east-1

# call this in case of errors
describe:
	aws cloudformation describe-stack-events --stack-name $(STACK_NAME)

release:
	@make bundle
	@make package
	@make deploy

clean:
	rm -rf "$(VENV_DIR)" "$(BASE)/var" "$(BASE)/__pycache__" "$(ZIP_FILE)"

