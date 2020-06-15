import factory
from faker import Faker

from timesheet import models

fake = Faker()


class RoleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Role

    title = fake.job()
    description = fake.sentence(nb_words=10)


class ProjectFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Project

    number = fake.pyint(1000)
    description = fake.sentence(nb_words=10)
    active = fake.boolean(chance_of_getting_true=75)


class GoalTypeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.GoalType

    type_ = fake.sentence(3)
    description = fake.sentence(10)


class EmployeeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Employee

    first_name = fake.first_name()
    last_name = fake.last_name()
    role = factory.SubFactory(RoleFactory)


class GoalFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Goal

    goal = "\n".join(fake.paragraphs(nb=4))
    ending_date = fake.date()
    type_ = factory.SubFactory(GoalTypeFactory)
    employee = factory.SubFactory(EmployeeFactory)


class TimesheetFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Timesheet

    date = fake.date()
    employee = factory.SubFactory(EmployeeFactory)
    project = factory.SubFactory(ProjectFactory)
    days = [1 for _ in range(7)]
