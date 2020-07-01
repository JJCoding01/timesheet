import pytest
#
# def string_or_none(string):
#     """Convert input string to None if it is empty, otherwise return original string"""
#     if string == '':
#         return None
#     return string

@pytest.mark.gui
def test_first_name(edit_name_dialog, employee):
    assert employee.first_name == edit_name_dialog.first_name


@pytest.mark.gui
def test_last_name(edit_name_dialog, employee):
    assert employee.last_name == edit_name_dialog.last_name


@pytest.mark.gui
def test_nickname(edit_name_dialog, employee):
    assert employee.nickname == edit_name_dialog.nickname


@pytest.mark.gui
def test_initials(edit_name_dialog, employee):
    assert employee.initials == edit_name_dialog.initials


@pytest.mark.gui
def test_username(edit_name_dialog, employee):
    assert employee.username == edit_name_dialog.username


@pytest.mark.gui
def test_email(edit_name_dialog, employee):
    assert employee.email == edit_name_dialog.email


@pytest.mark.gui
def test_role(edit_name_dialog, employee):
    assert employee.role.title == edit_name_dialog.role_dropdown.currentText()


@pytest.mark.gui
def test_active(edit_name_dialog, employee):
    assert employee.active == edit_name_dialog.active
