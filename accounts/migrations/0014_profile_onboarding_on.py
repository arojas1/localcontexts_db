# Generated by Django 3.1.13 on 2021-11-10 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20210928_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='onboarding_on',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]