# Generated by Django 3.1.13 on 2022-07-06 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0118_auto_20220706_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_privacy',
            field=models.CharField(choices=[('Discoverable', 'Discoverable'), ('Public', 'Public'), ('Private', 'Private')], max_length=20, null=True),
        ),
    ]