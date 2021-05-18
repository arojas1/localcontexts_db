# Generated by Django 3.0.7 on 2021-05-11 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0025_actionnotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institutionnotification',
            name='institution',
        ),
        migrations.RemoveField(
            model_name='institutionnotification',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='researchernotification',
            name='researcher',
        ),
        migrations.RemoveField(
            model_name='researchernotification',
            name='sender',
        ),
        migrations.DeleteModel(
            name='CommunityNotification',
        ),
        migrations.DeleteModel(
            name='InstitutionNotification',
        ),
        migrations.DeleteModel(
            name='ResearcherNotification',
        ),
    ]