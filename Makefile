include Python.mk
PROJECT = libcli
COV_FAIL_UNDER = 90
lint :: mypy
doc :: mkdoc-readme
mkdoc-readme:
	./mkdoc $(PROJECT) >README.md
.PHONY: mkdoc-readme
