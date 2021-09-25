from django.test import TestCase
from account.models import User
from timesheet.models import TimeSheet
from django.core.exceptions import ValidationError


class TimeSheetModelTest(TestCase):

    def setUp(self):
        self.mobile = "09121234567"
        self.username = "amir"
        self.password = "123"
        self.user = User.objects.create_user(self.mobile, self.username, self.password)
        self.timesheet = TimeSheet.objects.create(user=self.user, current_date="1400-10-10", enter_time="14:20:22")

    def test_datetime(self):
        self.assertEqual(self.timesheet.current_date, "1400-10-10")
        self.assertEqual(self.timesheet.enter_time,"14:20:22")
        self.assertEqual(self.timesheet.exit_time, None)

    def test_userinfo(self):
        self.assertEqual(self.user.mobile,self.mobile)