# Generated by Django 3.1.13 on 2022-09-09 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researchers', '0032_remove_researcher_projects'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='researcher',
            index=models.Index(fields=['user', 'image'], name='researchers_user_id_ea74ad_idx'),
        ),
    ]