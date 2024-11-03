include Python.mk
PROJECT = libcli
COV_FAIL_UNDER = 90
lint :: mypy
doc :: README.md
README.md:
	./mkdoc $(PROJECT) >$@
