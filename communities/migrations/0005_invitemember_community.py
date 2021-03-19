# Generated by Django 3.0.7 on 2020-12-16 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0004_invitemember'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitemember',
            name='community',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='community', to='communities.Community'),
        ),
    ]