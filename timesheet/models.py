import groups as groups
from django.db import models
from account.models import User
from django_jalali.db import models as jmodels
from django.utils import timezone
import jdatetime


class TimeSheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="timesheets" , limit_choices_to={"groups__name":"employee"} , verbose_name="نام کارمند")
    current_date = jmodels.jDateField(default=jdatetime.datetime.now().date(), verbose_name="تاریخ")
    enter_time = models.TimeField(default=None, verbose_name="ساعت ورود")
    exit_time = models.TimeField(default=None, verbose_name="ساعت خروج")

    def __str__(self):
        return self.user + " " + self.current_date

    class Meta:
        verbose_name = "ورود- خروج کارمند"
        verbose_name_plural = "ورود-خروج کارمندان"


class AccessPoint(models.Model):
    ssid = models.CharField(max_length=100, verbose_name="نام شبکه وایرلس روتر")
    bssid = models.CharField(max_length=100, verbose_name="مک آدرس روتر")
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.ssid

    class Meta:
        verbose_name = "تنظیمات روتر"
        verbose_name_plural = "تنظیمات روترها"