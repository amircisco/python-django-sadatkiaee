from django.db import models
from django.contrib.auth.models import Group
from account.models import User
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class Insurer(models.Model):
    name = models.CharField(max_length=200,verbose_name="نام و نام خانوادگی",blank=True)
    mobile = models.CharField(max_length=50,verbose_name="تلفن همراه",unique=True,blank=True,null=True)
    address = models.CharField(blank=True, null=True, max_length=300, verbose_name="آدرس")
    pelak = models.CharField(max_length=20, verbose_name="پلاک",blank=True,null=True)
    p1 = models.IntegerField( verbose_name="دو رقم اول پلاک",blank=True,null=True)
    p2 = models.CharField(max_length=5, verbose_name="حرف پلاک",blank=True,null=True)
    p3 = models.IntegerField( verbose_name="سه رقم پلاک",blank=True,null=True)
    p4 = models.IntegerField( verbose_name="ایران",blank=True,null=True)
    created_by = models.ForeignKey(User,related_name="user",on_delete=models.DO_NOTHING,verbose_name="ثبت شده توسط")

    def __str__(self):
        return str(self.name) + " " + str(self.mobile)

    class Meta:
        verbose_name = 'بیمه گذار'
        verbose_name_plural = 'بیمه گذاران'
        ordering = ('-id',)

class Visit(models.Model):
    year_choices = [(str(x), str(x)) for x in range(1399, 1410)]
    insurer = models.ForeignKey(Insurer, on_delete=models.DO_NOTHING, related_name='insurer',verbose_name="بیمه گذار")
    visitor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='visitor',
                                limit_choices_to={'groups__name': 'visitor'},verbose_name='بازدید کننده')
    year = models.CharField(verbose_name="سال", choices=year_choices, max_length=4, default='1400')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    finished = models.BooleanField(verbose_name="اتمام",default=False)

    @property
    def visitor_info(self):
        return {'id': self.visitor.id, 'name': self.visitor.name}

    def __str__(self):
        return str(self.insurer.name)

    @property
    def insurer_name(self):
        return self.insurer.name

    class Meta:
        verbose_name = 'بازدید'
        verbose_name_plural = 'بازدیدها'
        ordering = ('-id',)


class Image(models.Model):
    visit = models.ForeignKey(Visit,related_name="images",on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/%Y/%m/%d',verbose_name="تصویر")

    def __str__(self):
        return str(self.img)

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'
        ordering = ('-id',)


class Document(models.Model):
    user = models.ForeignKey(Insurer,on_delete=models.CASCADE,verbose_name="بیمه گذار")

    class Meta:
        verbose_name = 'مدرک(کارمندان)'
        verbose_name_plural = 'مدارک(کارمندان)'
        ordering = ('-id',)


class DocumentFile(models.Model):
    document = models.ForeignKey(Document,on_delete=models.CASCADE)
    file = models.FileField(upload_to="staff/documents/%Y/%m/%d",verbose_name="مدرک")

    class Meta:
        verbose_name = 'مدرک'
        verbose_name_plural = 'مدارک'


class InsurerDocument(models.Model):
    user = models.ForeignKey(Insurer,on_delete=models.CASCADE,verbose_name="بیمه گذار")

    class Meta:
        verbose_name = 'مدرک(بیمه گذاران)'
        verbose_name_plural = 'مدارک(بیمه گذاران)'
        ordering = ('-id',)

    def __str__(self):
        return self.user.

class InsurerDocumentFile(models.Model):
    document = models.ForeignKey(InsurerDocument,on_delete=models.CASCADE)
    file = models.FileField(upload_to="insurer/documents/%Y/%m/%d",verbose_name="مدرک")

    class Meta:
        verbose_name = 'مدرک'
        verbose_name_plural = 'مدارک'

