from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from timesheet.models import Base
from timesheet.conf import DATABASE_URI
from tests.timesheet import factories

engine = create_engine(DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)


def recreate_all():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def populate():

    session = Session()
    factories.RoleFactory._meta.sqlalchemy_session = session
    factories.ProjectFactory._meta.sqlalchemy_session = session
    factories.GoalTypeFactory._meta.sqlalchemy_session = session
    factories.GoalFactory._meta.sqlalchemy_session = session
    factories.EmployeeFactory._meta.sqlalchemy_session = session
    factories.EmployeeFactory._meta.sqlalchemy_session = session
    factories.EntryFactory._meta.sqlalchemy_session = session

    factories.GoalFactory.create_batch(10)
    factories.EntryFactory.create_batch(15)

    session.commit()
    session.close()


def main():
    recreate_all()
    populate()


if __name__ == "__main__":
    main()
