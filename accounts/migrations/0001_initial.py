# Generated by Django 3.0.7 on 2020-12-08 22:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, default='default.png', null=True, upload_to='photos/')),
                ('phone', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
                ('nationality', models.CharField(blank=True, max_length=60, null=True, verbose_name='nationality')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('city_or_town', models.CharField(blank=True, max_length=80, null=True, verbose_name='city or town')),
                ('job_title', models.CharField(blank=True, max_length=80, null=True, verbose_name='job title')),
                ('affiliation', models.CharField(blank=True, max_length=60, null=True, verbose_name='affiliation')),
                ('community_member', models.BooleanField(default=False, null=True)),
                ('is_researcher', models.BooleanField(default=False, null=True)),
                ('registration_reason', models.CharField(choices=[('', ''), ('community', 'Register a Community Account'), ('institution', 'Register an Institution Account'), ('researcher', 'Register a Research Account')], max_length=12, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]