
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column, Integer, Date, String, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Employee(Base):
    __tablename__ = "Employees"
    employee_id = Column("EmployeeID", Integer, primary_key=True)
    first_name = Column("FirstName", String(25), nullable=False)
    last_name = Column("LastName", String(25), nullable=False)
    nickname = Column("Nickname", String(15))
    username = Column("Username", String(25))
    initials = Column("Initials", String(3))
    active = Column("Active", Boolean, default=True)
    role_id = Column("RoleID", ForeignKey("Roles.RoleID"))
    role = relationship("Role", backref=backref("Employees", uselist=False))

    __table_args__ = (
        UniqueConstraint("FirstName", "LastName", name="emp_name"),
    )

    def __init__(
        self, first_name, last_name, nickname=None, initials=None, username=None, role=None
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.nickname = nickname
        self.role = role

        if initials is None:
            self.initials = f"{first_name[0]}{last_name[0]}".upper()
        else:
            self.initials = initials

        if username is None:
            self.username = f"{first_name[0]}{last_name}".lower()
        else:
            self.username = initials

    def __repr__(self):
        return f"{__class__.__name__}('{self.first_name}', '{self.last_name}', '{self.nickname}', '{self.initials}')"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Role(Base):
    __tablename__ = "Roles"
    role_id = Column("RoleID", Integer, primary_key=True)
    role = Column("Role", String(10), unique=True, nullable=False)
    description = Column("Description", String(50))

    def __init__(self, role, description=None):
        self.role = role
        self.description = description

    def __repr__(self):
        return f"{__class__.__name__}('{self.role}', '{self.description}')"


class Project(Base):
    __tablename__ = "Projects"
    project_id = Column("ProjectID", Integer, primary_key=True)
    number = Column("Number", Integer, unique=True, nullable=False)
    description = Column("Description", String(50))
    active = Column("Active", Boolean, default=True)

    def __init__(self, number, description):
        self.number = number
        self.description = description

    def __repr__(self):
        return f"{__class__.__name__}({self.number}, '{self.description}')"


class TimesheetMixin:

    timesheet_id = Column("TimesheetID", Integer, primary_key=True)
    ending_date = Column("EndingDate", Date, nullable=False)

    def __init__(self, date, employee, project, goal1, goal2, days):
        self.ending_date = date
        self.employee = employee
        self.project = project
        self.days = days
        (
            self.day1,
            self.day2,
            self.day3,
            self.day4,
            self.day5,
            self.day6,
            self.day7,
        ) = days

    def __repr__(self):
        return (
            f"{__class__.__name__}("
            f"date={self.ending_date}, "
            f"employee={self.employee}, "
            f"project={self.project}, "
            f"days=({self.day1}, {self.day2}, ...) ...)"
        )

    @declared_attr
    def __tablename__(self):
        return f"{self.__name__}s"

    @declared_attr
    def employee_id(self):
        return Column(
            "EmployeeID", Integer, ForeignKey("Employees.EmployeeID"), nullable=False
        )

    @declared_attr
    def employee(self):
        return relationship(
            "Employee", backref=backref(f"{self.__name__}"), uselist=False
        )

    @declared_attr
    def project_id(self):
        return Column(
            "ProjectID", Integer, ForeignKey("Projects.ProjectID"), nullable=True
        )

    @declared_attr
    def project(self):
        return relationship('Project', backref=backref(f'{self.__name__}', uselist=False))

    # add a column for each day of the week, keep these general, so the
    # first/last day can be customized at the front end. These will store the
    # hours related to the project
    day1 = Column("Day1", Float)
    day2 = Column("Day2", Float)
    day3 = Column("Day3", Float)
    day4 = Column("Day4", Float)
    day5 = Column("Day5", Float)
    day6 = Column("Day6", Float)
    day7 = Column("Day7", Float)

    # add goals
    goals1 = Column('Goals1', String(300))
    goals2 = Column('Goals2', String(300))


class TimesheetPending(TimesheetMixin, Base):
    __tablename__ = "TimesheetsPending"


class Timesheet(TimesheetMixin, Base):
    pass
