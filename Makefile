PROJECT = libcli
include Python.mk
lint:: mypy
doc::README.md
README.md:
	./mkdoc $(PROJECT) >$@

test :: cov_fail_under_90
cov_fail_under_90:
	python -m pytest --cov-fail-under 90 --cov=$(PROJECT) tests
