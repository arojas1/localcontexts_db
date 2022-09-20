# Generated by Django 3.1.13 on 2022-09-09 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0027_auto_20220909_2318'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='institution',
            name='institution_institu_168149_idx',
        ),
        migrations.AddIndex(
            model_name='institution',
            index=models.Index(fields=['id', 'institution_creator', 'image'], name='institution_id_225b15_idx'),
        ),
    ]