# Generated by Django 3.1.7 on 2021-06-14 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazdidkhodro', '0002_auto_20210614_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurer',
            name='p1',
            field=models.IntegerField(blank=True, null=True, verbose_name='دو رقم اول پلاک'),
        ),
        migrations.AlterField(
            model_name='insurer',
            name='p2',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='حرف پلاک'),
        ),
        migrations.AlterField(
            model_name='insurer',
            name='p3',
            field=models.IntegerField(blank=True, null=True, verbose_name='سه رقم پلاک'),
        ),
        migrations.AlterField(
            model_name='insurer',
            name='p4',
            field=models.IntegerField(blank=True, null=True, verbose_name='ایران'),
        ),
        migrations.AlterField(
            model_name='insurer',
            name='pelak',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='پلاک'),
        ),
    ]
