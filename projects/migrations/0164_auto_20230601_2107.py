# Generated by Django 3.1.13 on 2023-06-01 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0163_auto_20230525_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_privacy',
            field=models.CharField(choices=[('Contributor', 'Contributor'), ('Private', 'Private'), ('Public', 'Public')], max_length=20, null=True),
        ),
    ]