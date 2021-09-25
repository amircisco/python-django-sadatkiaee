from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from account.models import User
from timesheet.models import TimeSheet
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
import jdatetime


class ApiTimeSheetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("09196421676", "amir", "123")
        self.client = Client()

    def test_get_timesheet_auth(self):
        response = self.client.post(reverse('get_timesheet'), {'details':''})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_enter_timesheet(self):
        token = AccessToken.for_user(self.user)
        header = {
            'HTTP_AUTHORIZATION':'Bearer {}'.format(token)
        }
        response = self.client.post(reverse('enter_timesheet'), **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_enter_timesheet_auth(self):
        token = AccessToken.for_user(self.user)
        response = self.client.post(reverse('enter_timesheet'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_exit_timesheet(self):
        current_date = str(jdatetime.datetime.now().date())
        enter_time = str(jdatetime.datetime.now().time()).split(".")[0]
        TimeSheet.objects.create(user=self.user, current_date=current_date, enter_time=enter_time)
        token = AccessToken.for_user(self.user)
        header = {
            'HTTP_AUTHORIZATION':'Bearer {}'.format(token)
        }
        response = self.client.post(reverse('exit_timesheet'), **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


