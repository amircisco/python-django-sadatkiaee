# Generated by Django 3.1.7 on 2021-08-17 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jdatetime


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=jdatetime.datetime.now)),
                ('employee', models.ForeignKey(limit_choices_to={'groups__name': 'employee'}, on_delete=django.db.models.deletion.DO_NOTHING, related_name='employee', to=settings.AUTH_USER_MODEL, verbose_name='ارسال کننده')),
            ],
            options={
                'verbose_name': 'مدرک(کارمندان)',
                'verbose_name_plural': 'مدارک(کارمندان)',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Insurer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='نام و نام خانوادگی')),
                ('mobile', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='تلفن همراه')),
                ('address', models.CharField(blank=True, max_length=300, null=True, verbose_name='آدرس')),
                ('pelak', models.CharField(blank=True, max_length=20, null=True, verbose_name='پلاک')),
                ('p1', models.IntegerField(blank=True, null=True, verbose_name='دو رقم اول پلاک')),
                ('p2', models.CharField(blank=True, max_length=5, null=True, verbose_name='حرف پلاک')),
                ('p3', models.IntegerField(blank=True, null=True, verbose_name='سه رقم پلاک')),
                ('p4', models.IntegerField(blank=True, null=True, verbose_name='ایران')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='ثبت شده توسط')),
            ],
            options={
                'verbose_name': 'بیمه گذار',
                'verbose_name_plural': 'بیمه گذاران',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='InsurerDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazdidkhodro.insurer', verbose_name='بیمه گذار')),
            ],
            options={
                'verbose_name': 'مدرک(بیمه گذاران)',
                'verbose_name_plural': 'مدارک(بیمه گذاران)',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='MenuItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='نام منو')),
                ('link', models.CharField(max_length=500, verbose_name='لینک منو')),
            ],
            options={
                'verbose_name': 'منو اپلیکیشن',
                'verbose_name_plural': 'منو های اپلیکیشن',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(choices=[('1399', '1399'), ('1400', '1400'), ('1401', '1401'), ('1402', '1402'), ('1403', '1403'), ('1404', '1404'), ('1405', '1405'), ('1406', '1406'), ('1407', '1407'), ('1408', '1408'), ('1409', '1409')], default='1400', max_length=4, verbose_name='سال')),
                ('create_date', models.DateTimeField(default=jdatetime.datetime.now)),
                ('update_date', models.DateTimeField(default=jdatetime.datetime.now)),
                ('finished', models.BooleanField(default=False, verbose_name='اتمام')),
                ('insurer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='insurer', to='bazdidkhodro.insurer', verbose_name='بیمه گذار')),
                ('visitor', models.ForeignKey(limit_choices_to={'groups__name': 'visitor'}, on_delete=django.db.models.deletion.DO_NOTHING, related_name='visitor', to=settings.AUTH_USER_MODEL, verbose_name='بازدید کننده')),
            ],
            options={
                'verbose_name': 'بازدید',
                'verbose_name_plural': 'بازدیدها',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='MobileSignal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=25, verbose_name='نوع')),
                ('enter_date', models.DateTimeField(default=jdatetime.datetime.now, verbose_name=' ورود')),
                ('leave_date', models.DateTimeField(blank=True, default=None, null=True, verbose_name=' خروج')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bazdidkhodro.menuitems', verbose_name='لینک وارد شده')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'فعالیت کارمند',
                'verbose_name_plural': 'فعالیت های کارمندان',
            },
        ),
        migrations.CreateModel(
            name='InsurerDocumentFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='insurer/documents/%Y/%m/%d', verbose_name='مدرک')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazdidkhodro.insurerdocument')),
            ],
            options={
                'verbose_name': 'مدرک',
                'verbose_name_plural': 'مدارک',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='تصویر')),
                ('visit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='bazdidkhodro.visit')),
            ],
            options={
                'verbose_name': 'تصویر',
                'verbose_name_plural': 'تصاویر',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='DocumentFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='staff/documents/%Y/%m/%d', verbose_name='مدرک')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazdidkhodro.document')),
            ],
            options={
                'verbose_name': 'مدرک',
                'verbose_name_plural': 'مدارک',
            },
        ),
        migrations.AddField(
            model_name='document',
            name='insurer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazdidkhodro.insurer', verbose_name='بیمه گذار'),
        ),
    ]