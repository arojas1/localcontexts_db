# Generated by Django 3.1.13 on 2021-10-22 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tklabels', '0019_auto_20210830_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='TKNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]