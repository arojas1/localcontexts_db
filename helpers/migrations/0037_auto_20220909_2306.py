# Generated by Django 3.1.13 on 2022-09-09 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpers', '0036_labelversion_is_approved'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='connections',
            index=models.Index(fields=['community', 'institution', 'researcher'], name='helpers_con_communi_15ed73_idx'),
        ),
        migrations.AddIndex(
            model_name='entitiesnotified',
            index=models.Index(fields=['project'], name='helpers_ent_project_369ea5_idx'),
        ),
        migrations.AddIndex(
            model_name='notice',
            index=models.Index(fields=['project'], name='helpers_not_project_844147_idx'),
        ),
        migrations.AddIndex(
            model_name='projectcomment',
            index=models.Index(fields=['project'], name='helpers_pro_project_4a7394_idx'),
        ),
        migrations.AddIndex(
            model_name='projectstatus',
            index=models.Index(fields=['project'], name='helpers_pro_project_9d2572_idx'),
        ),
    ]
