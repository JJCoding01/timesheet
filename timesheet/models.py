"""
Module that defines the database schema and all the models (database tables)
required to create a timesheet.

"""
from sqlalchemy import UniqueConstraint
from sqlalchemy import (
    Column,
    Integer,
    Date,
    String,
    Boolean,
    ForeignKey,
    Float,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from timesheet.conf import EMAIL_DOMAIN


Base = declarative_base()


class Employee(Base):
    __tablename__ = "Employees"
    employee_id = Column("EmployeeID", Integer, primary_key=True)
    first_name = Column("FirstName", String(25), nullable=False)
    last_name = Column("LastName", String(25), nullable=False)
    nickname = Column("Nickname", String(15))
    username = Column("Username", String(25), nullable=False)
    initials = Column("Initials", String(3))
    email = Column("Email", String(25), unique=True, nullable=False)
    active = Column("Active", Boolean, default=True)
    role_id = Column("RoleID", ForeignKey("Roles.RoleID"))
    role = relationship("Role", backref=backref("Employees", uselist=False))

    __table_args__ = (UniqueConstraint("FirstName", "LastName", name="emp_name"),)

    def __init__(
        self,
        first_name,
        last_name,
        nickname=None,
        initials=None,
        username=None,
        email=None,
        role=None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.nickname = nickname
        self.role = role

        if initials is None:
            self.initials = f"{first_name[0]}{last_name[0]}".upper()
        else:
            self.initials = initials

        if username is None:
            self.username = f"{first_name[0]}{last_name}".lower()
        else:
            self.username = username

        if email is None:
            self.email = f"{first_name[0]}{last_name}{EMAIL_DOMAIN}".lower()
        else:
            self.email = email

    def __repr__(self):
        return (
            f"{__class__.__name__}("
            f"'{self.first_name}', "
            f"'{self.last_name}', "
            f"'{self.nickname}', "
            f"'{self.initials}')"
        )

    @property
    def full_name(self):
        """Read-only property that displays the fullname of Employee"""
        return f"{self.first_name} {self.last_name}"


class Role(Base):
    __tablename__ = "Roles"
    role_id = Column("RoleID", Integer, primary_key=True)
    title = Column("Title", String(75), unique=True, nullable=False)
    description = Column("Description", String(250))

    def __init__(self, title, description=None):
        self.title = title
        self.description = description

    def __repr__(self):
        return f"{__class__.__name__}('{self.title}', '{self.description}')"


class Project(Base):
    __tablename__ = "Projects"
    project_id = Column("ProjectID", Integer, primary_key=True)
    number = Column("Number", Integer, unique=True, nullable=False)
    description = Column("Description", String(50))
    active = Column("Active", Boolean, default=True)

    def __init__(self, number, description, active=True):
        self.number = number
        self.description = description
        self.active = active

    def __repr__(self):
        return (
            f"{__class__.__name__}({self.number}, '{self.description}', {self.active})"
        )


class GoalType(Base):
    __tablename__ = "GoalTypes"
    type_id = Column("TypeID", Integer, primary_key=True)
    type = Column("Type", String(50), nullable=False, unique=True)
    description = Column("Description", String(250))

    def __init__(self, type_, description=None):
        self.type = type_
        self.description = description

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.type}', '{self.description}')"


class Goal(Base):
    __tablename__ = "Goals"
    goal_id = Column("GoalID", Integer, primary_key=True)
    text = Column("Text", String(1500))
    ending_date = Column("EndingDate", Date, nullable=False)
    type_id = Column("TypeID", Integer, ForeignKey("GoalTypes.TypeID"), nullable=False)
    type = relationship("GoalType", backref=backref("Goals", uselist=True))
    employee_id = Column(
        "EmployeeID", Integer, ForeignKey("Employees.EmployeeID"), nullable=False,
    )
    employee = relationship("Employee", backref=backref("Goals", uselist=True))

    def __init__(self, text, ending_date, type_=None, employee=None):
        self.text = text
        self.ending_date = ending_date
        self.type = type_
        self.employee = employee

    def __repr__(self):
        return (
            f"Goal("
            f"goal='{self.goal}',"
            f"ending_date={self.ending_date},"
            f"type_={self.type},"
            f"employee={self.employee})"
        )


class Entry(Base):

    __tablename__ = "Entries"
    entry_id = Column("EntryID", Integer, primary_key=True)
    ending_date = Column("EndingDate", Date, nullable=False)
    note = Column("Note", String(125), nullable=True)
    employee_id = Column(
        "EmployeeID", Integer, ForeignKey("Employees.EmployeeID"), nullable=False
    )
    project_id = Column(
        "ProjectID", Integer, ForeignKey("Projects.ProjectID"), nullable=True
    )

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

    employee = relationship("Employee", backref=backref(f"Entries"), uselist=False)
    project = relationship("Project", backref=backref(f"Entries", uselist=True))

    def __init__(self, ending_date, note, employee, project, days):
        self.ending_date = ending_date
        self.note = note
        self.employee = employee
        self.project = project
        self.days = days

    def __repr__(self):
        return (
            f"{__class__.__name__}("
            f"ending_date={self.ending_date}, "
            f"note='{self.note}', "
            f"employee={self.employee}, "
            f"project={self.project}, "
            f"days={self.days}"
        )

    @property
    def days(self):
        try:
            return self._days
        except AttributeError:
            # self._days does not exist yet. This happens when the Entry object
            # was created from a query and the __init__ method is not ran
            self._days = [self.day1, self.day2, self.day3, self.day4, self.day5, self.day6, self.day7]
        return self._days

    @days.setter
    def days(self, values):
        if len(values) != 7:
            raise ValueError(f"Length of days must be 7, not {len(values)}")
        self._days = values

    @property
    def total_hours(self):
        return sum(self.days)

    @property
    def display_row(self):

        row = [self.project.number]
        row.extend(self.days)
        row.append(self.total_hours)
        row.append(self.note)
        return row
