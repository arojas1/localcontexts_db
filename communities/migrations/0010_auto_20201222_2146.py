# Generated by Django 3.0.7 on 2020-12-22 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0009_auto_20201218_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='is_approved',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='community_name',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='invitemember',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('editor', 'editor'), ('viewer', 'viewer')], max_length=8, null=True),
        ),
    ]