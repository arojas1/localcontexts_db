# Generated by Django 3.0.7 on 2021-07-08 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0035_auto_20210617_2200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noticestatus',
            name='bcnotice',
        ),
        migrations.RemoveField(
            model_name='noticestatus',
            name='community',
        ),
        migrations.RemoveField(
            model_name='noticestatus',
            name='tknotice',
        ),
        migrations.DeleteModel(
            name='NoticeComment',
        ),
        migrations.DeleteModel(
            name='NoticeStatus',
        ),
    ]
