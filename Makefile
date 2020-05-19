PACKAGE_NAME=timesheet

.PHONY: install docs lint-html tests

docs:
	cd docs && make html

install:
	python setup.py install

lint:
	black $(PACKAGE_NAME) --line-length=79

lint-tests:
	black tests --line-length=79
	pylint tests

tests:
	pytest --cov-report html --cov=$(PACKAGE_NAME) tests/$(PACKAGE_NAME)

tests-ci:
	pytest --cov-report html --cov=$(PACKAGE_NAME) tests/$(PACKAGE_NAME) -v

gui:
	pyuic5 -x $(PACKAGE_NAME)/gui/gui.ui -o $(PACKAGE_NAME)/gui/gui.py

run-gui:
	python $(PACKAGE_NAME)/gui/gui.py

start-gui:
	python $(PACKAGE_NAME)/gui/gui_commands.py
