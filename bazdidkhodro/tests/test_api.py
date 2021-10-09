import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from account.models import User
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def employee_user(db):
    mobile = "09191234567"
    username = "user1"
    password = "password1"
    group_name = "employee"
    user = User.objects.create_user(mobile, username, password)
    user.is_staff = True
    user.is_active = True
    user.groups.name = group_name
    user.save()
    return user


@pytest.fixture
def access_token_employee_user(employee_user):
    return AccessToken.for_user(employee_user)


def test_api_insurer_list_view(api_client, access_token_employee_user):
    url = reverse("bazdidkhodro:insurer_list_view")
    api_client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(access_token_employee_user))
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_insurer_create_view(api_client, access_token_employee_user):
    url = reverse("bazdidkhodro:insurer_create_view")
    data = {"p1":"22","p2":"ی","p3":"777","p4":"61"}
    api_client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(access_token_employee_user))
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK