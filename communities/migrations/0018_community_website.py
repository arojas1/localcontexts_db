# Generated by Django 3.0.7 on 2021-04-20 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0017_auto_20210325_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='website',
            field=models.URLField(blank=True, max_length=150, null=True),
        ),
    ]
