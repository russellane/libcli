PROJECT = libcli
include Python.mk
lint:: mypy
doc::README.md
README.md:
	./mkdoc $(PROJECT) >$@
