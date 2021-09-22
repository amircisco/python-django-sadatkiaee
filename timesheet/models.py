from django.db import models
from account.models import User
import jdatetime


class TimeSheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="timesheets" , verbose_name="نام کارمند")
    current_date = models.DateField(default=None, blank=True,null=True, verbose_name="تاریخ")
    enter_time = models.TimeField(default=None, verbose_name="ساعت ورود")
    exit_time = models.TimeField(default=None, blank=True, null=True, verbose_name="ساعت خروج")

    @property
    def current_date_jalali(self):
        return self.jcurrent_date(self.current_date)

    @staticmethod
    def gcurrent_date(date):
        current_date = str(date)
        if current_date.find("/") > -1 :
            arr_date = current_date.split("/")
            cur = jdatetime.datetime(year=int(arr_date[0]), month=int(arr_date[1]), day=int(arr_date[2])).togregorian().date()
        elif current_date.find("-") > -1 :
            arr_date = current_date.split("-")
            cur = jdatetime.datetime(year=int(arr_date[0]), month=int(arr_date[1]), day=int(arr_date[2])).togregorian().date()
        return str(cur)

    def jcurrent_date(self, date):
        current_date = str(date)
        if current_date.find("/") > -1 :
            arr_date = current_date.split("/")
            cur = jdatetime.datetime.fromgregorian(year=int(arr_date[0]), month=int(arr_date[1]), day=int(arr_date[2])).date()
        elif current_date.find("-") > -1 :
            arr_date = current_date.split("-")
            cur = jdatetime.datetime.fromgregorian(year=int(arr_date[0]), month=int(arr_date[1]), day=int(arr_date[2])).date()
        return str(cur)

    def __str__(self):
        return str(self.user) + " " + str(self.current_date)

    class Meta:
        verbose_name = "ورود- خروج کارمند"
        verbose_name_plural = "ورود-خروج کارمندان"


class AccessPoint(models.Model):
    ssid = models.CharField(max_length=100, verbose_name="نام شبکه وایرلس روتر")
    bssid = models.CharField(max_length=100, verbose_name="مک آدرس روتر")
    ip = models.CharField(max_length=100, verbose_name="آدرس آیپی روتر")
    subnet = models.CharField(max_length=100, verbose_name="آدرس سابنت روتر")
    status = models.BooleanField(default=True, verbose_name="وضعیت")

    def __str__(self):
        return self.ssid

    class Meta:
        verbose_name = "تنظیمات روتر"
        verbose_name_plural = "تنظیمات روترها"


class Commission(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام پورسانت")

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class CommissionAmount(Commission):
    amount = models.CharField(max_length=50, default=0, verbose_name="مبلغ")

    @property
    def commaamount(self):
        return "{:,.0f}".format(float(self.amount))

    class Meta:
        verbose_name = "پورسانت مبلغی"
        verbose_name_plural = "پورسانت ها مبلغی"


class CommissionPercentage(Commission):
    percentage = models.CharField(max_length=50, default=0, verbose_name="درصد")

    class Meta:
        verbose_name = "پورسانت درصدی"
        verbose_name_plural = "پورسانت ها درصدی"


class SalarySetting(models.Model):
    worktime = models.IntegerField(unique=True, verbose_name="حداکثر ساعت کاری", default=176)
    extraworktime = models.IntegerField(unique=True, verbose_name="حداکثر ساعت اضافه کاری", default=120)
    workamount = models.CharField(max_length=50, unique=True, verbose_name="دستمزد یک ساعت کاری", default=80000)
    extraworkamount = models.CharField(max_length=50, unique=True, verbose_name="دستمزد یک ساعت اضافه کاری", default=170000)

    @property
    def commaworkamount(self):
        return "{:,.0f}".format(float(self.workamount))

    @property
    def commaextraforkamount(self):
        return "{:,.0f}".format(self.extraworkamount)

    def verbose_name(self,fieldname):
        return self._meta.get_field(fieldname).verbose_name

    class Meta:
        verbose_name = "تنظمیات حقوق"
        verbose_name_plural = "تنظیمات حقوق"