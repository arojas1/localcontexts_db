# Generated by Django 3.1.13 on 2022-07-22 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpers', '0032_labelversion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labelversion',
            name='version_translated_text',
        ),
    ]