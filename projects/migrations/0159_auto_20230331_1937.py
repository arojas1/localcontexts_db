# Generated by Django 3.1.13 on 2023-03-31 19:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0158_auto_20230316_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_boundary_geojson',
            field=models.JSONField(blank=True, null=True, verbose_name='Project boundary GeoJSON'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_data_guid',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Project data GUID'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_privacy',
            field=models.CharField(choices=[('Private', 'Private'), ('Contributor', 'Contributor'), ('Public', 'Public')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='providers_id',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Provider's ID"),
        ),
        migrations.AlterField(
            model_name='project',
            name='publication_doi',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Publication DOI'),
        ),
        migrations.AlterField(
            model_name='project',
            name='related_projects',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='_project_related_projects_+', to='projects.Project', verbose_name='Related Projects'),
        ),
        migrations.AlterField(
            model_name='project',
            name='source_project_uuid',
            field=models.UUIDField(blank=True, db_index=True, null=True, verbose_name='Source Project UUID'),
        ),
        migrations.AlterField(
            model_name='project',
            name='unique_id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, null=True, unique=True, verbose_name='Unique ID (UUID)'),
        ),
        migrations.AlterField(
            model_name='project',
            name='urls',
            field=models.JSONField(blank=True, null=True, verbose_name='URLs'),
        ),
    ]