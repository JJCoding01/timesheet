from pathlib import Path
from PyQt5 import QtWidgets, uic

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from timesheet import models as db
from timesheet.conf import DATABASE_URI

engine = create_engine(DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)

UIFilename = Path(__file__).parent / "EditNameDialog.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(UIFilename)


class EditNameDialog(QtWidgets.QDialog, Ui_MainWindow):
    def __init__(self, employee_id):
        QtWidgets.QDialog.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.session = Session()
        print(employee_id)
        self.employee = (
            self.session.query(db.Employee)
            .filter_by(employee_id=employee_id)
            .first()
        )
        # self.role = self.employee.role
        # print(self.role)
        self.first_name.setText(self.employee.first_name)
        self.last_name.setText(self.employee.last_name)
        self.initials.setText(self.employee.initials)
        self.username.setText(self.employee.username)
        self.nickname.setText(self.employee.nickname)

        self.active.setChecked(self.employee.active)
        self.employee_id.setText(employee_id)

        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)

    def ok(self):
        # employee = db.Employee(
        self.employee.first_name = self.first_name.text()
        self.employee.last_name = self.last_name.text()
        self.employee.nickname = self.nickname.text()
        self.employee.initials = self.initials.text()
        self.employee.username = self.username.text()

        self.session.commit()
        self.session.close()

        #     role=self.role)

        # print(employee)
        # employee = db.Employee(self.first_name.getText())
        print("ok button was pressed")

    def cancel(self):
        print("cancel button was pressed")
        self.session.close()
