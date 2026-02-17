include Python.mk
PROJECT = libcli
COV_FAIL_UNDER = 90
lint :: mypy
doc :: mkdoc-readme
.PHONY: mkdoc-readme
mkdoc-readme:
	pdm run ./mkdoc $(PROJECT) >README.md
