# Generated by Django 3.0.7 on 2021-06-15 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0027_community_state_or_province'),
    ]

    operations = [
        migrations.RenameField(
            model_name='community',
            old_name='town',
            new_name='city_or_town',
        ),
    ]
