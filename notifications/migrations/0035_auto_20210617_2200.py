# Generated by Django 3.0.7 on 2021-06-17 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0034_auto_20210617_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticecomment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]