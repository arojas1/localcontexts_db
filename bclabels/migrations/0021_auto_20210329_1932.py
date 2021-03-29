# Generated by Django 3.0.7 on 2021-03-29 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bclabels', '0020_bclabel_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='bclabel',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bclabel_approver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bclabel',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bclabel_creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
