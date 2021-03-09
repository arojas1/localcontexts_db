from django.db import models
from institutions.models import Institution
from communities.models import Community
from researchers.models import Researcher

class Project(models.Model):
    TYPES = (
        ('Item', 'Item'),
        ('Collection', 'Collection'),
        ('Expedition', 'Expedition'),
        ('Publication', 'Publication'),
    )
    project_type = models.CharField(max_length=20, null=True, choices=TYPES)
    title = models.TextField(null=True)
    description = models.TextField(null=True)
    # principal_investigator = models.CharField(max_length=100, blank=True, null=True)
    # principal_investigator_affiliation = models.CharField(max_length=100, blank=True, null=True)
    project_contact = models.CharField(max_length=100, blank=True, null=True)
    project_contact_email = models.EmailField(max_length=100, blank=True, null=True)
    publication_doi = models.CharField(max_length=200, blank=True, null=True)
    project_data_guid = models.CharField(max_length=200, blank=True, null=True)
    recommended_citation = models.CharField(max_length=200, blank=True, null=True)
    geome_project_id = models.IntegerField(blank=True, null=True)
    # source = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    publication_date = models.DateField(null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    is_public = models.BooleanField(default=True, null=True)
    bclabels = models.ManyToManyField("bclabels.BCLabel", verbose_name="BC Labels", blank=True, related_name="project_labels")

    def has_labels(self):
        bc_labels = self.bclabels.count()
        if bc_labels > 0:
            return True
        else:
            return False

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-date_added',)

class ProjectContributors(models.Model):
    project = models.OneToOneField(Project, null=True, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, null=True, blank=True, on_delete=models.DO_NOTHING)
    community = models.ForeignKey(Community, null=True, blank=True, on_delete=models.DO_NOTHING)
    researcher = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.project) + ' ' + str(self.community) + ' ' + str(self.researcher)

    class Meta:
        verbose_name = 'Project Contributors'
        verbose_name_plural = 'Project Contributors'

