# Generated by Django 3.0.7 on 2021-06-22 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0030_joinrequest_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='support_document',
            field=models.FileField(blank=True, null=True, upload_to='communities/support-files'),
        ),
    ]