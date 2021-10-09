from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from account.models import User
from timesheet.models import TimeSheet
from rest_framework_simplejwt.tokens import AccessToken
import datetime
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def employee_user(db):
    user = User.objects.create_user("09191234567", "user1", "123")
    user.is_staff = True
    user.is_active = True
    user.groups.name = "employee"
    user.save()
    return user


@pytest.fixture
def access_token_employee_user(employee_user):
    return AccessToken.for_user(employee_user)


def test_get_timesheet_auth(api_client, access_token_employee_user):
    url = reverse('get_timesheet')
    data = {"details":{"ssid":""}}
    api_client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(access_token_employee_user))
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_enter_timesheet(api_client, access_token_employee_user):
    url = reverse('enter_timesheet')
    api_client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(access_token_employee_user))
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK


def test_enter_timesheet_auth(api_client, access_token_employee_user):
    url = reverse('enter_timesheet')
    api_client.credentials(HTTP_AUTHORIZATION="Bearer {}".format("aaaa"))
    response = api_client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_exit_timesheet(db,api_client, access_token_employee_user, employee_user):
    current_date = str(datetime.datetime.now().date())
    enter_time = str(datetime.datetime.now().time()).split(".")[0]
    TimeSheet.objects.create(user=employee_user, current_date=current_date, enter_time=enter_time)
    url = reverse('exit_timesheet')
    api_client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(access_token_employee_user))
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK









