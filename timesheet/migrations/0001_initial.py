# Generated by Django 3.1.7 on 2021-09-25 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssid', models.CharField(max_length=100, verbose_name='نام شبکه وایرلس روتر')),
                ('bssid', models.CharField(max_length=100, verbose_name='مک آدرس روتر')),
                ('ip', models.CharField(max_length=100, verbose_name='آدرس آیپی روتر')),
                ('subnet', models.CharField(max_length=100, verbose_name='آدرس سابنت روتر')),
                ('status', models.BooleanField(default=True, verbose_name='وضعیت')),
            ],
            options={
                'verbose_name': 'تنظیمات روتر',
                'verbose_name_plural': 'تنظیمات روترها',
            },
        ),
        migrations.CreateModel(
            name='CommissionAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='نام پورسانت')),
                ('amount', models.CharField(default=0, max_length=50, verbose_name='مبلغ')),
            ],
            options={
                'verbose_name': 'پورسانت مبلغی',
                'verbose_name_plural': 'پورسانت ها مبلغی',
            },
        ),
        migrations.CreateModel(
            name='CommissionPercentage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='نام پورسانت')),
                ('percentage', models.CharField(default=0, max_length=50, verbose_name='درصد')),
            ],
            options={
                'verbose_name': 'پورسانت درصدی',
                'verbose_name_plural': 'پورسانت ها درصدی',
            },
        ),
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_date', models.DateField(blank=True, default=None, null=True, verbose_name='تاریخ')),
                ('enter_time', models.TimeField(default=None, verbose_name='ساعت ورود')),
                ('exit_time', models.TimeField(blank=True, default=None, null=True, verbose_name='ساعت خروج')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timesheets', to=settings.AUTH_USER_MODEL, verbose_name='نام کارمند')),
            ],
            options={
                'verbose_name': 'ورود- خروج کارمند',
                'verbose_name_plural': 'ورود-خروج کارمندان',
            },
        ),
        migrations.CreateModel(
            name='CalcSalaryTimeSheetProxy',
            fields=[
            ],
            options={
                'verbose_name': 'محاسبه حقوق و دستمزد',
                'verbose_name_plural': 'محاسبه حقوق و دستمزد',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('timesheet.timesheet',),
        ),
    ]
