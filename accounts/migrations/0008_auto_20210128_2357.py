# Generated by Django 3.0.7 on 2021-01-28 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210127_2126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='signupinvitation',
            options={'ordering': ('-date_sent',), 'verbose_name': 'Sign Up Invitation', 'verbose_name_plural': 'Sign Up Invitations'},
        ),
    ]
