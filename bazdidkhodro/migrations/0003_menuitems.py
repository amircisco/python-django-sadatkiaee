# Generated by Django 3.1.7 on 2021-07-30 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazdidkhodro', '0002_auto_20210713_0110'),
    ]

    operations = [
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
            },
        ),
    ]
