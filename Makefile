include Python.mk
PROJECT = libcli
lint :: mypy
doc :: mkdoc-readme
.PHONY: mkdoc-readme
mkdoc-readme:
	pdm run ./mkdoc $(PROJECT) >README.md
install::;@:
