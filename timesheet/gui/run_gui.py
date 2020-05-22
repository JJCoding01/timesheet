import sys

from pathlib import Path
from datetime import datetime, timedelta
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, uic

path = Path(__file__).parent
UIFilename = Path(__file__).parent / "mainWindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(UIFilename)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.fullname.editingFinished.connect(self.name_changed)
        self.date.dateChanged.connect(self.set_goal_labels)
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.exit)
        self.set_goal_labels()
        self.OK.clicked.connect(self.ok)
        self.Cancel.clicked.connect(self.exit)

    def set_goal_labels(self):
        date_str = self.date.text()
        date = datetime.strptime(date_str, "%b %d %Y")
        _format = "%b %d"

        sat_date = date.strftime(_format)
        last_week = (date - timedelta(days=6)).strftime(_format)
        tomorrow = (date + timedelta(days=1)).strftime(_format)
        next_week = (date + timedelta(days=7)).strftime(_format)
        this_week = f"Goals for this week ({last_week} to {sat_date})"
        next_week = f"Goals for next week ({tomorrow} to {next_week})"
        self.labelThisWeekGoals.setText(this_week)
        self.labelFutureGoals.setText(next_week)

    def name_changed(self):
        print(f"the name has been changed to: {self.fullname.text()}")

    @staticmethod
    def ok():
        print('ok button pressed')

    @staticmethod
    def exit():
        print('cancel button was pressed')
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
