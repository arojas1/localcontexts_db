# Generated by Django 3.0.7 on 2021-09-30 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0019_auto_20210924_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='contact_number',
        ),
    ]