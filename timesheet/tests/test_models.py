from account.models import User
from timesheet.models import TimeSheet
import pytest


@pytest.fixture
def create_user(db):
    mobile = "09121234567"
    username = "amir"
    password = "123"
    return User.objects.create_user(mobile,username,password)


@pytest.fixture
def create_timesheet(db,create_user):
    return TimeSheet.objects.create(user=create_user, current_date="1400-10-10", enter_time="14:20:22")


def test_datetime(create_timesheet):
    assert create_timesheet.current_date == "1400-10-10"
    assert create_timesheet.enter_time == "14:20:22"
    assert create_timesheet.exit_time == None


def test_userinfo_mobile(create_user):
    assert create_user.mobile == "09121234567"


def test_userinfo_username(create_user):
    assert create_user.username == "amir"