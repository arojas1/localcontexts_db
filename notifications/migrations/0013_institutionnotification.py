# Generated by Django 3.0.7 on 2021-04-13 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0009_auto_20210325_2256'),
        ('notifications', '0012_auto_20210128_2357'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstitutionNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('notification_type', models.CharField(choices=[('Requests', 'requests'), ('Labels', 'labels'), ('Connections', 'Connections')], max_length=20, null=True)),
                ('reference_id', models.CharField(blank=True, max_length=10, null=True)),
                ('viewed', models.BooleanField(default=False)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('institution', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.Institution')),
            ],
            options={
                'verbose_name': 'Institution Notification',
                'verbose_name_plural': 'Institution Notifications',
                'ordering': ('-created',),
            },
        ),
    ]