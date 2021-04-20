# Generated by Django 3.0.7 on 2021-04-14 18:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bclabels', '0021_auto_20210329_1932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bclabel',
            name='modified_text',
        ),
        migrations.AddField(
            model_name='bcnotice',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]