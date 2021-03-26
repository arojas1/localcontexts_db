# Generated by Django 3.0.7 on 2021-03-25 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0016_remove_community_community_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='contact_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='contact_name',
            field=models.CharField(max_length=80, null=True),
        ),
    ]