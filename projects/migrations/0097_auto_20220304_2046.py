# Generated by Django 3.1.13 on 2022-03-04 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0096_auto_20220304_2018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='providers_project_id',
            new_name='providers_id',
        ),
        migrations.AlterField(
            model_name='project',
            name='project_privacy',
            field=models.CharField(choices=[('Discoverable', 'Discoverable'), ('Private', 'Private'), ('Public', 'Public')], max_length=20, null=True),
        ),
    ]