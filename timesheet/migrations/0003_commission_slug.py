# Generated by Django 3.1.7 on 2021-09-18 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0002_auto_20210918_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='نام با حروف لاتین'),
        ),
    ]
