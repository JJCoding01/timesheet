from sqlalchemy import UniqueConstraint

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Employee(Base):
    __tablename__ = "Employees"
    employee_id = Column("EmployeeID", Integer, primary_key=True)
    first_name = Column("FirstName", String(25), nullable=False)
    last_name = Column("LastName", String(25), nullable=False)
    nickname = Column("Nickname", String(15))
    initials = Column("Initials", String(3))
    active = Column("Active", Boolean, default=True)
    role_id = Column("RoleID", ForeignKey("Roles.RoleID"))
    role = relationship("Role", backref=backref("Employees", uselist=False))

    __table_args__ = (
        UniqueConstraint("FirstName", "LastName", name="emp_name"),
    )

    def __init__(
        self, first_name, last_name, nickname=None, initials=None, role=None
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.nickname = nickname
        self.role = role

        if initials is None:
            self.initials = f"{first_name[0]}{last_name[0]}".upper()
        else:
            self.initials = initials

    def __repr__(self):
        return f"{__class__.__name__}('{self.first_name}', '{self.last_name}', '{self.nickname}', '{self.initials}')"


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

    def __init__(self, number, description):
        self.number = number
        self.description = description

    def __repr__(self):
        return f"{__class__.__name__}({self.number}, '{self.description}')"
