from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, mobile, username, password, **extra_fields):
        if not mobile:
            raise ValueError(_('the mobile must be set'))
        user = self.model(mobile=mobile, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile, username, password, **extra_fields):
        user = self.create_user(mobile, username, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True,verbose_name="فعال بودن")
    is_staff = models.BooleanField(default=False,verbose_name="کارمند")
    is_superuser = models.BooleanField(default=False,verbose_name="مدیر کل")
    groups = models.ManyToManyField(
        Group,
        verbose_name="گروه کاربری",
        blank=True,
        related_name="groups",
    )
    username = models.CharField(max_length=255,unique=True,verbose_name="نام کاربری")
    email = models.EmailField(max_length=255, unique=True,verbose_name="ایمیل")
    mobile = models.CharField(max_length=255,unique=True,verbose_name="شماره موبایل")
    password = models.CharField(max_length=1000,verbose_name="رمز عبور")
    #date_joined = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ثبت در سیستم")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ثبت در سیستم")
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['password','username']

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class FamilyManager(models.Manager):
    """
    Lets us do querysets limited to families that have
    currently enrolled students, e.g.:
        Family.has_students.all()
    """
    def get_query_set(self):
        return super(FamilyManager, self).get_query_set().filter(student__enrolled=True).distinct()


class Family(Group):
    notes = models.TextField(blank=True,verbose_name="توضیحات")

    # Two managers for this model - the first is default
    # (so all families appear in the admin).
    # The second is only invoked when we call
    # Family.has_students.all()
    objects = models.Manager()
    has_students = FamilyManager()

    class Meta:
        verbose_name = "گروه کاربری"
        verbose_name_plural = "گروه های کاربری"
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_name_group(self,key):
        try:
            d = {'visitor':'بازدید کننده','employee':'کارمند'}
            return d.get(key)
        except:
            return ""