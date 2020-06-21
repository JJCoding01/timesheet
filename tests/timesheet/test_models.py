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


def test_create_timesheet(create_and_get):
    ts, db_ts = create_and_get(factories.TimesheetFactory, models.Timesheet)
    assert ts.ending_date == db_ts.ending_date
    assert ts.employee.employee_id == db_ts.employee.employee_id
    assert ts.project.project_id == db_ts.project.project_id
