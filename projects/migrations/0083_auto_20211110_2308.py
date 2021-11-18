# Generated by Django 3.1.13 on 2021-11-10 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0082_auto_20211105_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_privacy',
            field=models.CharField(choices=[('Discoverable', 'Discoverable'), ('Public', 'Public'), ('Private', 'Private')], max_length=20, null=True),
        ),
    ]