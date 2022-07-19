# Generated by Django 3.1.13 on 2022-07-19 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0121_auto_20220718_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_privacy',
            field=models.CharField(choices=[('Public', 'Public'), ('Private', 'Private'), ('Discoverable', 'Discoverable')], max_length=20, null=True),
        ),
    ]
