#
# def string_or_none(string):
#     """Convert input string to None if it is empty, otherwise return original string"""
#     if string == '':
#         return None
#     return string


def test_first_name(app, employee):
    assert employee.first_name == app.first_name


def test_last_name(app, employee):
    assert employee.last_name == app.last_name


def test_nickname(app, employee):
    assert employee.nickname == app.nickname


def test_initials(app, employee):
    assert employee.initials == app.initials


def test_username(app, employee):
    assert employee.username == app.username


def test_email(app, employee):
    assert employee.email == app.email


def test_role(app, employee):
    assert employee.role.title == app.role_dropdown.currentText()


def test_active(app, employee):
    assert employee.active == app.active
