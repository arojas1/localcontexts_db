# Generated by Django 3.1.13 on 2023-06-28 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0030_auto_20230607_2059'),
        ('helpers', '0051_auto_20230626_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionsCareNoticePolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_document', models.FileField(blank=True, null=True, upload_to='institutions/support-files')),
                ('url', models.URLField(null=True, unique=True, verbose_name='Website URL')),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.institution')),
            ],
            options={
                'verbose_name': 'Collections Care Notice URL',
                'verbose_name_plural': 'Collections Care Notice URLs',
            },
        ),
    ]
