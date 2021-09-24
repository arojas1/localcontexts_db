# Generated by Django 3.0.7 on 2021-09-24 22:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researchers', '0026_researcher_orcid_auth_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researcher',
            name='description',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(200)]),
        ),
    ]
