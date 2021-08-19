# Generated by Django 3.0.7 on 2021-08-19 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0034_auto_20210819_1251'),
        ('researchers', '0025_remove_researcher_location'),
        ('institutions', '0017_auto_20210615_2153'),
        ('communities', '0033_auto_20210625_2030'),
        ('helpers', '0004_noticecomment_noticestatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice_type', models.CharField(choices=[('biocultural', 'biocultural'), ('traditional_knowledge', 'traditional_knowledge')], max_length=50, null=True)),
                ('img_url', models.URLField(blank=True, null=True)),
                ('default_text', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('communities', models.ManyToManyField(blank=True, related_name='notice_communities', to='communities.Community')),
                ('placed_by_institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.Institution')),
                ('placed_by_researcher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='researchers.Researcher')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_notice', to='projects.Project')),
            ],
            options={
                'verbose_name': 'Notice',
                'verbose_name_plural': 'Notices',
                'ordering': ('-created',),
            },
        ),
    ]
