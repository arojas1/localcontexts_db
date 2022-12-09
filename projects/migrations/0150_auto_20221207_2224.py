# Generated by Django 3.1.13 on 2022-12-07 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0149_auto_20221207_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_privacy',
            field=models.CharField(choices=[('Private', 'Private'), ('Public', 'Public'), ('Discoverable', 'Discoverable')], max_length=20, null=True),
        ),
    ]
