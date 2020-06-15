import pytest

from PyQt5.QtCore import QDate

from timesheet.gui.MainWindow import MainWindow


@pytest.fixture()
def app():
    # app_ = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    yield window


def test_default_values(app):
    assert app.fullname.text() == ""
    assert app.id.text() == ""
    assert app.date.text() == "Jan 01 2020"
    assert app.goals1.toPlainText() == ""
    assert app.goals2.toPlainText() == ""
    assert app.labelThisWeekGoals.text() == "Goals for this week (Dec 26 to Jan 01)"
    assert app.labelFutureGoals.text() == "Goals for next week (Jan 02 to Jan 08)"

    # QTest.mouseClick(app.OK, Qt.LeftButton)
    # QTest.mouseClick(app.Cancel, Qt.LeftButton)


def test_this_week_goal_labels(app):

    assert app.date.text() == "Jan 01 2020"
    assert app.labelThisWeekGoals.text() == "Goals for this week (Dec 26 to Jan 01)"

    # now change the date and validate that the goal label was updated properly
    app.date.setDate(QDate(2020, 5, 23))  # May 23 2020
    assert app.date.text() == "May 23 2020"
    assert app.labelThisWeekGoals.text() == "Goals for this week (May 17 to May 23)"


def test_future_week_goal_labels(app):
    assert app.date.text() == "Jan 01 2020"
    assert app.labelFutureGoals.text() == "Goals for next week (Jan 02 to Jan 08)"

    # now change the date and validate that the goal label was updated properly
    app.date.setDate(QDate(2020, 5, 23))  # May 23 2020
    assert app.date.text() == "May 23 2020"
    assert app.labelFutureGoals.text() == "Goals for next week (May 24 to May 30)"
