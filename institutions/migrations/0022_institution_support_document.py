# Generated by Django 3.0.7 on 2021-10-01 20:21

from django.db import migrations, models
import institutions.models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0021_auto_20211001_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='support_document',
            field=models.FileField(blank=True, null=True, upload_to=institutions.models.get_file_path),
        ),
    ]