# Generated by Django 3.0.7 on 2021-03-30 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tklabels', '0003_auto_20210329_1932'),
        ('projects', '0007_auto_20210329_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='tklabels',
            field=models.ManyToManyField(blank=True, related_name='project_tklabels', to='tklabels.TKLabel', verbose_name='TK Labels'),
        ),
    ]