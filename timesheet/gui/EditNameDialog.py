from pathlib import Path
from PyQt5 import QtWidgets, uic
from timesheet.conf import Session

UIFilename = Path(__file__).parent / "EditNameDialog.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(UIFilename)


class EditNameDialog(QtWidgets.QDialog, Ui_MainWindow):
    def __init__(self, employee, roles, session=None):
        QtWidgets.QDialog.__init__(self)
        Ui_MainWindow.__init__(self)
        self.employee = employee
        self.roles = roles
        if session is None:
            self.session = Session()
        else:
            self.session = session

        self.setupUi()

        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)

    # noinspection PyPep8Naming
    def setupUi(self):
        super(EditNameDialog, self).setupUi(self)

        self.first_name.setText(self.employee.first_name)
        self.last_name.setText(self.employee.last_name)
        self.initials.setText(self.employee.initials)
        self.username.setText(self.employee.username)
        self.nickname.setText(self.employee.nickname)
        self.email.setText(self.employee.email)
        self.active.setChecked(self.employee.active)
        self.employee_id.setText(str(self.employee.employee_id))

        # populate dropdown with all roles
        self.__populate_role_dropdown()

        # select proper role for current employee
        self.role_dropdown.setCurrentIndex(
            self.__roles[self.employee.role.title]["index"]
        )

    def __populate_role_dropdown(self):
        """Populate role dropdown with all roles"""

        self.__roles = {}
        for k, role in enumerate(self.roles):
            self.__roles.setdefault(role.title, {"id": role.role_id, "index": k})
            self.role_dropdown.addItem(f"{role.title}")

    def ok(self):
        self.employee.first_name = self.first_name.text()
        self.employee.last_name = self.last_name.text()
        self.employee.nickname = self.nickname.text()
        self.employee.initials = self.initials.text()
        self.employee.email = self.email.text()
        self.employee.username = self.username.text()
        self.employee.active = self.active.isChecked()

        # get the role id
        self.employee.role_id = self.__roles[self.role_dropdown.currentText()]["id"]

        self.session.commit()
        self.session.close()
        print("ok button was pressed")

    def cancel(self):
        print("cancel button was pressed")
        self.session.close()
