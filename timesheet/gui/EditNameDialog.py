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

        self.first_name = self.employee.first_name
        self.last_name = self.employee.last_name
        self.initials = self.employee.initials
        self.username = self.employee.username
        self.nickname = self.employee.nickname
        self.email = self.employee.email
        self.active = self.employee.active
        self.employee_id_field.setText(str(self.employee.employee_id))

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

    @property
    def first_name(self):
        text = self.first_name_field.text()
        if text == "":
            return None
        return text

    @first_name.setter
    def first_name(self, name):
        name = name if name is not None else ""
        self.first_name_field.setText(name)

    @property
    def last_name(self):
        text = self.last_name_field.text()
        if text == "":
            return None
        return text

    @last_name.setter
    def last_name(self, name):
        name = name if name is not None else ""
        self.last_name_field.setText(name)

    @property
    def nickname(self):
        text = self.nickname_field.text()
        if text == "":
            return None
        return text

    @nickname.setter
    def nickname(self, name):
        name = name if name is not None else ""
        self.nickname_field.setText(name)

    @property
    def initials(self):
        text = self.initials_field.text()
        if text == "":
            return None
        return text

    @initials.setter
    def initials(self, name):
        name = name if name is not None else ""
        self.initials_field.setText(name)

    @property
    def username(self):
        text = self.username_field.text()
        if text == "":
            return None
        return text

    @username.setter
    def username(self, name):
        name = name if name is not None else ""
        self.username_field.setText(name)

    @property
    def email(self):
        text = self.email_field.text()
        if text == "":
            return None
        return text

    @email.setter
    def email(self, address):
        address = address if address is not None else ""
        self.email_field.setText(address)

    @property
    def active(self):
        return self.active_field.isChecked()

    @active.setter
    def active(self, bool):
        self.active_field.setChecked(bool)

    def ok(self):
        self.employee.first_name = self.first_name
        self.employee.last_name = self.last_name
        self.employee.nickname = self.nickname
        self.employee.initials = self.initials
        self.employee.email = self.email
        self.employee.username = self.username
        self.employee.active = self.active

        # get the role id
        self.employee.role_id = self.__roles[self.role_dropdown.currentText()]["id"]

        try:
            self.session.commit()
        except Exception as e:
            print(e)
        print("ok button was pressed")

    def cancel(self):
        print("cancel button was pressed")
        self.session.close()
