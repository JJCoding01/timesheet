from pathlib import Path
import csv
import random, string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from timesheet.models import Base, Employee, Role, Project


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


def recreate_all():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def populate():
    Session = sessionmaker(bind=engine)
    session = Session()

    roles = [Role(*role) for role in get_test_data("fake_roles.csv")]
    employees = [
        Employee(*name, role=roles[random.randrange(len(roles))])
        for name in get_test_data("fake_names.csv")
    ]
    projects = [Project(n, get_random_string(15)) for n in range(1000, 1500)]

    for role in roles:
        session.add(role)

    for employee in employees:
        session.add(employee)

    for project in projects:
        session.add(project)

    session.commit()
    session.close()


def main():
    recreate_all()
    populate()


if __name__ == "__main__":
    main()
