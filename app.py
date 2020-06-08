import sys
import datetime
from PyQt5.QtWidgets import QApplication

from timesheet.gui.MainWindow import MainWindow
from timesheet import models as db
from timesheet.conf import DATABASE_URI

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
# from timesheet.gui.EditNameDialog import EditNameDialog

engine = create_engine(DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)


def main():
    session = Session()

    date = datetime.date(2020, 3, 11)
    timesheets = session.query(db.Timesheet).filter(
            db.Timesheet.employee_id == 2).filter(db.Timesheet.ending_date == date)

    for timesheet in timesheets:
        employee = timesheet.employee
        project = timesheet.project
        days = timesheet.days
        # now, consolidate all items into a single iterable
        row = [project.number]
        row.extend(timesheet.days)
        row.append(timesheet.total_hrs)
        row.append(project.description)
        print(row, timesheet.get_row)
        # print(timesheet)
        # print(timesheet.ending_date, timesheet.total_hrs)
        # print(project.number, days, timesheet.total_hrs, project.description)

    # goal = session.query(models.Goal).all()
    # emp = session.query(db.Employee).filter_by(employee_id = 2).first()

    # ts = session.query(db.Timesheet).filter(db.Timesheet.employee_id == 2).all()
    # print(ts)

    # for t in ts:
    #     # emp = t.employee
    #     print(t)
    # print(ts)
    #
    # goal_type = session.query(db.GoalType).filter_by(type_id=2).first()
    # date = datetime.date(2020, 1, 1)
    #
    # print(goal_type, emp)
    # goal = db.Goal('some goal', date, goal_type, emp)
    # print(goal)
    # goal = db.Goal(self.goals2.toPlainText(),ending_date=self.get_date(), type=goal_type, employee=self.employee)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    # main()
