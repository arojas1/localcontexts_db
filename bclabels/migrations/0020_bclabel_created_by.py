# Generated by Django 3.0.7 on 2021-03-03 21:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bclabels', '0019_auto_20210224_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='bclabel',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]