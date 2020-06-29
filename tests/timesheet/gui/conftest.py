import sys

import pytest
from PyQt5.QtWidgets import QApplication

from tests.timesheet import factories

from timesheet.gui.EditNameDialog import EditNameDialog


@pytest.fixture()
def employee(session):
    roles = factories.RoleFactory.create_batch(4)
    emp = factories.EmployeeFactory.create()
    emp.active = True
    emp.role = roles[2]
    yield emp


@pytest.fixture(scope="function")
def app(employee):
    app_ = QApplication(sys.argv)

    window = EditNameDialog(employee=employee, roles=[employee.role])
    window.show()
    yield window
    # sys.exit(app_.exec_())
