import sys


from pathlib import Path
from datetime import datetime, timedelta

from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox


from sqlalchemy import and_

from timesheet.gui.EditNameDialog import EditNameDialog
from timesheet import models as db
from timesheet.conf import Session

UIFilename = Path(__file__).parent / "MainWindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(UIFilename)


def showDialog(message="", title="Sample title", icon=QMessageBox.Information):
    msgBox = QMessageBox()
    msgBox.setIcon(icon)
    msgBox.setText(message)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    return msgBox.exec()


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.total_column = 8

    def flags(self, index):
        if index.column() == self.total_column or index.row() == self.rowCount() - 1:
            return Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        headers = [
            "Project number",
            "Sun",
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Total",
            "Description",
        ]
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(headers[section])

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._data[0])

    def data(self, index, role):
        value = self._data[index.row()][index.column()]
        if role == Qt.BackgroundColorRole:
            if index.row() % 2 == 0:
                return QtGui.QColor("lightgray")

        if index.column() == 0 and index.row() != self.rowCount() - 1:
            return self._format_project_numbers(index, role)
        if index.column() == self.total_column:
            return self._format_totals(index, role)
        if index.row() == self.rowCount() - 1:
            return self._format_totals(index, role)
        if index.column() == self.columnCount() - 1:
            return self._format_description(index, role)

        return self._format_hours(index, role)

    def _format_project_numbers(self, index, role):
        value = self._data[index.row()][index.column()]
        if role == Qt.DisplayRole:
            try:
                value = int(value)
                return f"{value:.0f}"
            except (ValueError, TypeError):
                return str(value)
        if role == Qt.ToolTipRole:
            return f"tooltip for {value}"
        # if role == Qt.StatusTipRole:
        #     return f'this is the status bar tip for project {value}'
        if role == Qt.DecorationRole:
            return QtGui.QColor("green")
        if role == Qt.FontRole:
            return QtGui.QFont("Times", 10, QtGui.QFont.Bold)
        if role == Qt.EditRole:
            return value

    def _format_totals(self, index, role):
        value = self._data[index.row()][index.column()]
        if role == Qt.DisplayRole:
            if value == "":
                return ""
            else:
                return f"{value:.2f}"
        # if role == Qt.BackgroundColorRole:
        #     return QtGui.QColor('gray')
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        if role == Qt.FontRole:
            return QtGui.QFont("Times", 10, QtGui.QFont.Bold)

    def _format_description(self, index, role):
        value = self._data[index.row()][index.column()]
        if role == Qt.DisplayRole:
            return value
        if role == Qt.FontRole:
            return QtGui.QFont("Times", 10)
        if role == Qt.EditRole:
            return value

    def _format_hours(self, index, role):
        value = self._data[index.row()][index.column()]
        if role == Qt.DisplayRole:
            if isinstance(value, (float, int)):
                return f"{value:0.2f}"
            return value
        if role == Qt.StatusTipRole:
            return f"Enter hours for project"

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            print("edit data", value)
            if index.column() == 9:  # description/notes column
                self._data[index.row()][index.column()] = value
                return True
            if index.column() == 0:  # project number column
                if len(str(value)) != 6:
                    print("invalid project number: {value}")
                else:
                    try:
                        self._data[index.row()][index.column()] = int(value)
                    except ValueError:
                        print(f"could not update with float. using default: {value}")
                return True
            # for all other columns...
            try:
                self._data[index.row()][index.column()] = float(value)
            except ValueError:
                print(f"could not update with int. using default: {value}")
                response = showDialog(
                    message=f"invalid entry: {value}\ndo you want to continue?",
                    title="Invalid Entry",
                    icon=QMessageBox.Warning,
                )
                if response == QMessageBox.Ok:
                    self._data[index.row()][index.column()] = value
        return True


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.session = Session()
        self.__employee = None
        self.__roles = None

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

        # ------------------
        self.data = [
            [111456, 3.25, 1, 2, 6, 2, 3, 4, 23, "some description"],
            [222456, 2, 4, 2, 3, 2, 3, 4, 27, "row 2 description"],
            [333456, 4, 4, 3, 5, 2, 3, 4, 27, "row 2 description"],
            [444456, 8, 4, 4, 6, 2, 3, 4, 27, "row 2 description"],
            ["", 6, 8, 10, 12, 4, 6, 8, 27, ""],  # totals row
        ]
        self.model = TableModel(self.data)
        self.tableView.setModel(self.model)
        header = self.tableView.horizontalHeader()

        for x in range(8):
            header.setSectionResizeMode(x, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(9, QtWidgets.QHeaderView.Stretch)

    @property
    def employee(self):
        if self.__employee is None or self.employee_id != self.__employee.employee_id:
            employee_id = self.employee_id.text()
            self.__employee = (
                self.session.query(db.Employee)
                .filter_by(employee_id=employee_id)
                .first()
            )
        return self.__employee

    @property
    def roles(self):
        if self.__roles is None:
            self.__roles = self.session.query(db.Role).all()
        return self.__roles

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

            # goal = db.Goal(
            #     text, self.get_date(), type=goal_type, employee=self.employee
            # )
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
            # goal = db.Goal(
            #     text, self.get_date(), type=goal_type, employee=self.employee
            # )
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
        # self.edit_name_dialog = EditNameDialog(self.employee_id.text())
        print('employee starting edit dialog', self.employee)
        try:
            self.edit_name_dialog = EditNameDialog(self.employee, self.roles, session=self.session)
            self.edit_name_dialog.exec()
        except Exception as e:
            print(e)

    def populate_table(self):
        # timesheets = (
        #     self.session.query(db.Timesheet)
        #     .filter(db.Timesheet.employee_id == self.employee.employee_id)
        #     .filter(db.Timesheet.ending_date == self.get_date())
        # )
        #
        # self.tableWidget.setRowCount(0)
        # for r, timesheet in enumerate(timesheets):
        #     self.tableWidget.insertRow(r)
        #     for c, column in enumerate(timesheet.get_row):
        #         self.tableWidget.setItem(r, c, QtWidgets.QTableWidgetItem(str(column)))
        pass

    # @staticmethod
    def ok(self):
        print(self.data)
        self.session.commit()
        self.session.close()
        self.exit()

    # @staticmethod
    def exit(self):
        self.session.rollback()
        self.session.close()
        sys.exit()
