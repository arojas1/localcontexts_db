# Generated by Django 3.0.7 on 2021-08-10 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bclabels', '0034_bclabel_img_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='bcnotice',
            name='default_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
