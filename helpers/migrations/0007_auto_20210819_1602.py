# Generated by Django 3.0.7 on 2021-08-19 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpers', '0006_auto_20210819_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='notice_type',
            field=models.CharField(choices=[('biocultural', 'biocultural'), ('traditional_knowledge', 'traditional_knowledge')], max_length=50, null=True),
        ),
    ]