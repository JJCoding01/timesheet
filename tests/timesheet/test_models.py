import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from timesheet import models
from tests.timesheet import factories

engine = create_engine("sqlite://")  # create in-memory database
Session = sessionmaker()


@pytest.fixture(scope="module")
def connection():
    _connection = engine.connect()
    models.Base.metadata.create_all(engine)
    yield _connection
    _connection.close()
    models.Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def session(connection):
    transaction = connection.begin()
    _session = Session(bind=connection)
    factories.TimesheetFactory._meta.sqlalchemy_session = _session
    factories.EmployeeFactory._meta.sqlalchemy_session = _session
    factories.GoalFactory._meta.sqlalchemy_session = _session
    factories.GoalTypeFactory._meta.sqlalchemy_session = _session
    factories.RoleFactory._meta.sqlalchemy_session = _session
    factories.ProjectFactory._meta.sqlalchemy_session = _session
    yield _session
    _session.close()
    transaction.rollback()


@pytest.fixture()
def create_and_get(session):
    """
    Fixture to create factory in database, then retrieve the item from database

    This allows tests to be done that validates that the model was created in
    the database as expected. Things such as relationships can be tested this
    way.
    """

    def create(factory, model):
        f = factory.create()
        db_f = session.query(model).one()
        return f, db_f

    yield create


def test_create_role(create_and_get):
    role, db_role = create_and_get(factories.RoleFactory, models.Role)
    assert role.title == db_role.title
    assert role.description == db_role.description


def test_create_project(create_and_get):
    project, db_project = create_and_get(factories.ProjectFactory, models.Project)
    assert project.number == db_project.number
    assert project.description == db_project.description
    assert project.active == db_project.active


def test_create_employee(create_and_get):
    employee, db_employee = create_and_get(factories.EmployeeFactory, models.Employee)
    assert employee.role.role_id is not None
    assert employee.first_name == db_employee.first_name
    assert employee.role.role_id == db_employee.role.role_id


def test_create_goal_type(create_and_get):
    goal_type, db_goal_type = create_and_get(factories.GoalTypeFactory, models.GoalType)
    assert goal_type.type == db_goal_type.type
    assert goal_type.description == db_goal_type.description


def test_create_goal(create_and_get):
    goal, db_goal = create_and_get(factories.GoalFactory, models.Goal)
    assert goal.text == db_goal.text
    assert goal.ending_date == db_goal.ending_date
    assert goal.employee.employee_id == db_goal.employee.employee_id
    assert goal.type.type_id == db_goal.type.type_id


def test_create_entry(create_and_get):
    entry, db_entry = create_and_get(factories.EntryFactory, models.Entry)
    assert entry.employee_id == db_entry.employee_id
    assert entry.ending_date == db_entry.ending_date
    assert entry.project_id == db_entry.project_id


@pytest.mark.parametrize("lengths", [0, 1, 2, 8])
def test_entry_invalid_day_count(lengths):
    with pytest.raises(ValueError):
        factories.EntryFactory(days=[2 for _ in range(lengths)])


@pytest.mark.parametrize("daily_hours", [1, 2, 5, 9, 12])
def test_entry_sum_hours(daily_hours):
    expected_total = daily_hours * 7
    e = factories.EntryFactory(days=[daily_hours for _ in range(7)])
    assert e.total_hours == expected_total


def test_display_row():
    entry = factories.EntryFactory.build()
    expected_display_row = [entry.project.number]
    expected_display_row.extend(entry.days)
    expected_display_row.append(entry.total_hours)
    expected_display_row.append(entry.project.description)

    assert len(expected_display_row) == len(entry.display_row)
    for expected, actual in zip(expected_display_row, entry.display_row):
        assert expected == actual


def test_employee_nickname():
    emp_default = factories.EmployeeFactory.build()
    assert emp_default.nickname is None

    emp = factories.EmployeeFactory(nickname="Bill")
    assert emp.nickname == "Bill"


def test_employee_initials():
    emp_default = factories.EmployeeFactory(first_name="William", last_name="Rodgers")
    assert emp_default.initials == "WR"

    emp = factories.EmployeeFactory(initials="WTR")
    assert emp.initials == "WTR"


def test_employee_username():
    emp_default = factories.EmployeeFactory(first_name="William", last_name="Rodgers")
    assert emp_default.username == "wrodgers"

    emp = factories.EmployeeFactory(username="rodgersusername")
    assert emp.username == "rodgersusername"


def test_employee_email():
    emp_default = factories.EmployeeFactory(first_name="William", last_name="Rodgers")
    assert emp_default.email == "wrodgers@example.com"

    emp = factories.EmployeeFactory(email="will@example.com")
    assert emp.email == "will@example.com"
