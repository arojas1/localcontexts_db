from django.contrib import admin
from .models import BCLabel, BCNotice


class BCNoticeAdmin(admin.ModelAdmin):
    list_display = ('project', 'placed_by_researcher', 'placed_by_institution', 'created')

class BCLabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'community', 'created_by', 'is_approved', 'created')

admin.site.register(BCLabel, BCLabelAdmin)
admin.site.register(BCNotice, BCNoticeAdmin)
