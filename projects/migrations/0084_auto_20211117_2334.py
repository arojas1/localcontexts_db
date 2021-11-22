# Generated by Django 3.1.13 on 2021-11-17 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0083_auto_20211110_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_privacy',
            field=models.CharField(choices=[('Public', 'Public'), ('Discoverable', 'Discoverable'), ('Private', 'Private')], max_length=20, null=True),
        ),
    ]
