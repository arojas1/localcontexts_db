# Generated by Django 3.1.13 on 2022-12-07 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpers', '0044_auto_20221207_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcomment',
            name='sender_affiliation',
            field=models.CharField(blank=True, max_length=350),
        ),
    ]
