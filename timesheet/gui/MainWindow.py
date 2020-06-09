import sys

from pathlib import Path
from datetime import datetime, timedelta
from PyQt5 import QtWidgets, uic, QtGui

# from PyQt5 import QtGui

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

from timesheet.gui.EditNameDialog import EditNameDialog
from timesheet import models as db
from timesheet.conf import DATABASE_URI

engine = create_engine(DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)

UIFilename = Path(__file__).parent / "MainWindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(UIFilename)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.session = Session()
        self.__employee = None

        # self.fullname.editingFinished.connect(self.name_changed)
        self.date_field.dateChanged.connect(self.date_changed)
        self.editNameButton.clicked.connect(self.edit_name)
        self.employee_id.textChanged.connect(self.set_name)

        self.goals1.textChanged.connect(self.goal1_change)
        self.goals2.textChanged.connect(self.goal2_change)
        self.set_goal_labels()
        self.OK.clicked.connect(self.ok)
        self.Cancel.clicked.connect(self.exit)

        self.employee_id.setText("2")

        self.populate_table()

    @property
    def employee(self):
        if self.__employee is None:
            employee_id = self.employee_id.text()
            self.__employee = (
                self.session.query(db.Employee)
                .filter_by(employee_id=employee_id)
                .first()
            )
        return self.__employee

    def date_changed(self):
        self.set_goal_labels()
        self.populate_goal1()
        self.populate_goal2()
        self.populate_table()

    def get_goal(self):
        employee_id = self.employee_id.text()
        date = self.get_date()
        goals = self.session.query(db.Goal).filter(
            and_(db.Goal.employee_id == employee_id, db.Goal.ending_date == date)
        )
        return goals

    def populate_goal1(self):
        goals = self.get_goal()
        goals = goals.filter(db.Goal.type_id == 1)
        goals = goals.first()
        if goals is not None:
            self.goals1.setPlainText(goals.goal)
        else:
            self.goals1.setPlainText("")

    def populate_goal2(self):
        goals = self.get_goal()
        goals = goals.filter(db.Goal.type_id == 2)
        goals = goals.first()
        if goals is not None:
            self.goals2.setPlainText(goals.goal)
        else:
            self.goals2.setPlainText("")

    def goal1_change(self):
        goal = self.get_goal().filter(db.Goal.type_id == 1).first()
        if goal is not None:
            goal.goal = self.goals1.toPlainText()
        else:
            text = self.goals1.toPlainText()
            if text == "":
                return
            goal_type = self.session.query(db.GoalType).filter_by(type_id=1).first()
            # print('text', text)
            # print('date', self.get_date())
            # print('goal type', goal_type, goal_type.type_id)
            # print('employee', self.employee)

            goal = db.Goal(
                text, self.get_date(), type=goal_type, employee=self.employee
            )
            # print(goal)
            self.session.add(goal)
            print("end creating goal")

    def goal2_change(self):
        goal = self.get_goal().filter(db.Goal.type_id == 2).first()
        if goal is not None:
            print("found some goal here")
            goal.goal = self.goals2.toPlainText()
        else:
            print("no goal2 found. it should be created for ", self.employee)
            text = self.goals2.toPlainText()
            if text == "":
                return
            goal_type = self.session.query(db.GoalType).filter_by(type_id=2).first()
            goal = db.Goal(
                text, self.get_date(), type=goal_type, employee=self.employee
            )
            self.session.add(goal)

    def get_date(self):
        date_str = self.date_field.text()
        # date = datetime.strptime(date_str, "%b %d %Y")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return date

    def set_goal_labels(self):
        # date_str = self.date_field.text()
        # date = datetime.strptime(date_str, "%b %d %Y")
        _format = "%b %d"
        date = self.get_date()
        sat_date = date.strftime(_format)
        last_week = (date - timedelta(days=6)).strftime(_format)
        tomorrow = (date + timedelta(days=1)).strftime(_format)
        next_week = (date + timedelta(days=7)).strftime(_format)
        this_week = f"Goals for this week ({last_week} to {sat_date})"
        next_week = f"Goals for next week ({tomorrow} to {next_week})"
        self.labelThisWeekGoals.setText(this_week)
        self.labelFutureGoals.setText(next_week)

    def set_name(self):
        # employee_id = self.employee_id.text()
        # session = Session()
        # self.employee = session.query(db.Employee).filter_by(employee_id=employee_id).first()
        self.fullname.setText(self.employee.full_name)

    def edit_name(self):
        self.edit_name_dialog = EditNameDialog(self.employee_id.text())
        self.edit_name_dialog.exec()

    def populate_table(self):
        timesheets = (
            self.session.query(db.Timesheet)
            .filter(db.Timesheet.employee_id == self.employee.employee_id)
            .filter(db.Timesheet.ending_date == self.get_date())
        )

        self.tableWidget.setRowCount(0)
        for r, timesheet in enumerate(timesheets):
            self.tableWidget.insertRow(r)
            for c, column in enumerate(timesheet.get_row):
                self.tableWidget.setItem(r, c, QtWidgets.QTableWidgetItem(str(column)))

    # @staticmethod
    def ok(self):
        self.session.commit()
        self.session.close()
        self.exit()

    # @staticmethod
    def exit(self):
        self.session.rollback()
        self.session.close()
        sys.exit()
