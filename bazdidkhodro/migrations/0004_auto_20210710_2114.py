# Generated by Django 3.1.7 on 2021-07-10 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bazdidkhodro', '0003_auto_20210710_1707'),
    ]

    operations = [
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
        migrations.AlterModelOptions(
            name='document',
            options={'ordering': ('-id',), 'verbose_name': 'مدرک(کارمندان)', 'verbose_name_plural': 'مدارک(کارمندان)'},
        ),
        migrations.AlterModelOptions(
            name='documentfile',
            options={'verbose_name': 'مدرک', 'verbose_name_plural': 'مدارک'},
        ),
        migrations.AlterField(
            model_name='document',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazdidkhodro.insurer', verbose_name='بیمه گذار'),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='file',
            field=models.FileField(upload_to='staff/documents/%Y/%m/%d', verbose_name='مدرک'),
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
    ]
