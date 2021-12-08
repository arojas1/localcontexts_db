# Generated by Django 3.1.13 on 2021-12-02 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0084_auto_20211117_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_privacy',
            field=models.CharField(choices=[('Discoverable', 'Discoverable'), ('Private', 'Private'), ('Public', 'Public')], max_length=20, null=True),
        ),
    ]