# Generated by Django 3.1.13 on 2021-11-05 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0039_community_approved_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
