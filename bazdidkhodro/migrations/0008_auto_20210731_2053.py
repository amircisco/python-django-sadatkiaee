# Generated by Django 3.1.7 on 2021-07-31 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bazdidkhodro', '0007_auto_20210731_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobilesignal',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bazdidkhodro.menuitems', verbose_name='لینک وارد شده'),
        ),
        migrations.AlterField(
            model_name='mobilesignal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]