PACKAGE_NAME=timesheet

.PHONY: install docs lint-html tests

docs:
	cd docs && make html

install:
	python setup.py install

lint:
	black $(PACKAGE_NAME)
	pylint $(PACKAGE_NAME)

lint-tests:
	black tests
	pylint tests

tests:
	pytest --cov-report html --cov=$(PACKAGE_NAME) tests/$(PACKAGE_NAME)

test-gui:
	pytest --cov-report html --cov=$(PACKAGE_NAME) tests/timesheet/gui

tests-ci:
	pytest --cov-report html --cov=$(PACKAGE_NAME) tests/$(PACKAGE_NAME) -v

gui:
	pyuic5 -x $(PACKAGE_NAME)/gui/mainWindow.ui -o $(PACKAGE_NAME)/gui/main_window.py

run-gui:
	python $(PACKAGE_NAME)/gui/gui.py

start-gui:
	python $(PACKAGE_NAME)/gui/gui_commands.py
