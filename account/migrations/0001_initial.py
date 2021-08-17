# Generated by Django 3.1.7 on 2021-08-17 14:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('notes', models.TextField(blank=True, verbose_name='توضیحات')),
            ],
            options={
                'verbose_name': 'گروه کاربری',
                'verbose_name_plural': 'گروه های کاربری',
                'ordering': ['name'],
            },
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال بودن')),
                ('is_staff', models.BooleanField(default=False, verbose_name='کارمند')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='مدیر کل')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='نام کاربری')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='ایمیل')),
                ('mobile', models.CharField(max_length=255, unique=True, verbose_name='شماره موبایل')),
                ('password', models.CharField(max_length=1000, verbose_name='رمز عبور')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ ثبت در سیستم')),
                ('groups', models.ManyToManyField(blank=True, related_name='groups', to='auth.Group', verbose_name='گروه کاربری')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
            },
        ),
    ]
