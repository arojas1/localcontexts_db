# Generated by Django 3.0.7 on 2020-12-28 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('communities', '0010_auto_20201222_2146'),
    ]

    operations = [
        migrations.CreateModel(
            name='BCDefaultLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_type', models.CharField(choices=[('provenance', 'Provenance BC Label (BC P)'), ('commercialization', 'Open to Commercialization BC Label (BC C)'), ('collaboration', 'Open to Collaboration BC Label (BC OC)'), ('consent_verified', 'Consent Verified BC Label (BC CV)'), ('multiple_community', 'Multiple Community BC Label (BC MC)'), ('research', 'Research Use BC Label (BC R)')], max_length=20, null=True)),
                ('name', models.CharField(max_length=90, null=True, verbose_name='label name')),
                ('default_text', models.TextField(blank=True, null=True)),
                ('community', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='communities.Community')),
            ],
        ),
    ]