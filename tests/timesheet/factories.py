from datetime import datetime
import factory
from faker import Faker

from timesheet import models

fake = Faker()


class RoleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Role

    title = factory.Sequence(lambda n: fake.job())
    description = factory.Sequence(lambda n: fake.sentence(nb_words=10))


class ProjectFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Project

    number = factory.Sequence(lambda n: 1000 + n)
    description = factory.Sequence(lambda n: fake.sentence(nb_words=5))
    active = factory.Sequence(lambda n: fake.boolean(chance_of_getting_true=75))


class GoalTypeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.GoalType

    type_ = factory.Sequence(lambda n: fake.sentence(3))
    description = factory.Sequence(lambda n: fake.sentence(7))


class EmployeeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Employee

    first_name = factory.Sequence(lambda n: fake.first_name())
    last_name = factory.Sequence(lambda n: fake.last_name())
    role = factory.SubFactory(RoleFactory)


class EntryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Entry

    ending_date = factory.Sequence(lambda n: datetime.strptime(fake.date(), "%Y-%m-%d"))
    note = factory.Sequence(lambda n: fake.sentence(nb_words=5))
    employee = factory.SubFactory(EmployeeFactory)
    project = factory.SubFactory(ProjectFactory)
    days = [1 for _ in range(7)]


class GoalFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Goal

    text = "\n".join(fake.paragraphs(nb=4))
    ending_date = factory.Sequence(lambda n: datetime.strptime(fake.date(), "%Y-%m-%d"))
    type_ = factory.SubFactory(GoalTypeFactory)
    employee = factory.SubFactory(EmployeeFactory)
