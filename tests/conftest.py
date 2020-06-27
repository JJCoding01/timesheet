import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tests.timesheet import factories
from timesheet import models

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
    factories.EmployeeFactory._meta.sqlalchemy_session = _session
    factories.GoalFactory._meta.sqlalchemy_session = _session
    factories.GoalTypeFactory._meta.sqlalchemy_session = _session
    factories.RoleFactory._meta.sqlalchemy_session = _session
    factories.ProjectFactory._meta.sqlalchemy_session = _session
    factories.EntryFactory._meta.sqlalchemy_session = _session
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
