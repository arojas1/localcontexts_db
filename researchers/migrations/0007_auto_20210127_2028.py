# Generated by Django 3.0.7 on 2021-01-27 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0013_auto_20210120_2254'),
        ('institutions', '0004_delete_userinstitution'),
        ('researchers', '0006_auto_20210126_2315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='contributor',
        ),
        migrations.CreateModel(
            name='ProjectContributors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='communities.Community')),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='institutions.Institution')),
                ('project', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='researchers.Project')),
            ],
            options={
                'verbose_name': 'Project Contributors',
                'verbose_name_plural': 'Project Contributors',
            },
        ),
    ]