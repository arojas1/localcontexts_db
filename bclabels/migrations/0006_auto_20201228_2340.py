# Generated by Django 3.0.7 on 2020-12-28 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bclabels', '0005_bclabel_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bclabel',
            name='default_text',
            field=models.TextField(null=True),
        ),
    ]