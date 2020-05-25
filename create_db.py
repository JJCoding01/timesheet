
from pathlib import Path
import csv
import random, string
import datetime
from datetime import timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from timesheet.models import Base, Employee, Role, Project, Timesheet


engine = create_engine("sqlite:///test.db", echo=False)


def get_test_data(filename):
    path = Path(".") / "tests" / "data" / filename
    with open(path, "r", newline="") as f:
        file = csv.reader(f)
        next(file, None)  # skip header row
        item_list = [(*row,) for row in file]
    return item_list


def get_random_string(word_count):
    def random_word(length):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(length))

    return " ".join(
        [random_word(random.randrange(10)) for _ in range(word_count)]
    )

def load_fake_roles():
    return [Role(*role) for role in get_test_data("fake_roles.csv")]

def load_fake_employees(roles):
    employees = [
        Employee(*name, role=roles[random.randrange(len(roles))])
        for name in get_test_data("fake_names.csv")
    ]
    return employees

def generate_fake_projects(n):
    return [Project(n, get_random_string(15)) for n in range(1000, 1500)]

def generate_fake_timesheets(n_weeks, n_projects, employees, projects):
    timesheets = []
    date = datetime.date(2020, 1, 1)
    for week in range(n_weeks):
        date += timedelta(days=7)
        for k in range(n_projects):  # have 100 line items (projects/employee)
            # get a tuple of hours for each day where the hours may be None for
            # some of the days
            days = tuple(random.randint(1, 9) if random.randint(0, 6) % 2 == 0 else None for _ in range(7))
            employee = employees[random.randint(0, len(employees) - 1)]
            project = projects[random.randint(0, len(projects) - 1)]
            timesheets.append(Timesheet(date, employee, project, days))
    return timesheets

def recreate_all():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def populate():

    roles = load_fake_roles()
    employees = load_fake_employees(roles)
    projects = generate_fake_projects(1000)
    timesheets = generate_fake_timesheets(52, 100, employees, projects)

    Session = sessionmaker(bind=engine)
    session = Session()
    for role in roles:
        session.add(role)

    for employee in employees:
        session.add(employee)

    for project in projects:
        session.add(project)

    for timesheet in timesheets:
        session.add(timesheet)

    session.commit()
    session.close()


def main():
    recreate_all()
    populate()

if __name__ == "__main__":
    main()
