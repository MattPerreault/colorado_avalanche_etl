START_DIR := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))

deps:
	pip install -Ur requirements.txt
