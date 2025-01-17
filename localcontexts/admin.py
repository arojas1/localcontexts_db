import itertools, calendar
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, timezone
from django.db.models.functions import TruncMonth, Extract
from django.db.models import Count, F, ExpressionWrapper, DurationField
from django.contrib import admin
from django.utils.translation import gettext as _
from django.apps import apps
from django.template.response import TemplateResponse
from django.http import Http404

from accounts.models import Profile, UserAffiliation, SignUpInvitation
from rest_framework_api_key.admin import APIKey, APIKeyModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin
from django_countries.fields import CountryField
from bclabels.models import BCLabel
from communities.models import Community, InviteMember, JoinRequest
from helpers.models import *
from institutions.models import Institution
from notifications.models import UserNotification, ActionNotification
from projects.models import *
from researchers.models import Researcher
from tklabels.models import TKLabel

# ADMIN HOMEPAGE
class MyAdminSite(admin.AdminSite):
    site_header = 'Local Contexts Hub Administration'
    index_title = 'Dashboard'
    site_title = 'Local Contexts Hub Admin'

    def index(self, request, context=None):
        otc_notices = OpenToCollaborateNoticeURL.objects.select_related('researcher', 'institution').all().order_by('-added')
        otc_notices_count = otc_notices.count()

        # How many projects were created by which account
        # FIXME: "column institutions_institution.ror_id does not exist"
        # for project in ProjectCreator.objects.select_related('institution', 'community', 'researcher').all():
        #     if project.institution:
        #         community_projects += 1
        #     if project.community:
        #         institution_projects += 1
        #     if project.researcher:
        #         researcher_projects += 1
        # projects_count = community_projects + institution_projects + researcher_projects

        context = { 
            'otc_notices' : otc_notices, 
            'otc_notices_count': otc_notices_count
        }
        context.update(counts())
        context.update(dataCharts())
        context.update(user_activity())
        context.update(project_activity())
        context.update(inactive_users())

        return super().index(request, context)
    
    # change the title of the page (the name that shows on the tab)
    def app_index(self, request, app_label, extra_context=None):
        app_dict = self._build_app_dict(request, app_label)
        if not app_dict:
            raise Http404('The requested admin page does not exist.')
        # Sort the models alphabetically within each app.
        app_dict['models'].sort(key=lambda x: x['name'])
        app_name = apps.get_app_config(app_label).verbose_name
        context = {
            **self.each_context(request),
            'title': _('%(app)s') % {'app': app_name},
            'app_list': [app_dict],
            'app_label': app_label,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.app_index_template or [
            'admin/%s/app_index.html' % app_label,
            'admin/app_index.html'
        ], context)

admin_site = MyAdminSite(name='lc-admin')

# DASHBOARD VIEWS
def counts():
    users_total = recent_users_count = country_count = projects_count = 0

    #Registered Users
    users_total = User.objects.count()
    recent_users_count = User.objects.filter(date_joined__gte=datetime.now(tz=timezone.utc) - timedelta(days=30)).count()

    # TODO: Change to Researcher, Inst, Comm account country count
    users_by_country = Profile.objects.filter(country__isnull=False).distinct('country').values('country')
    institutions_by_country = Institution.objects.filter(country__isnull=False).distinct('country').values('country')
    communities_by_country = Community.objects.filter(country__isnull=False).distinct('country').values('country')
    countries_list = []
    for country in users_by_country:
        if country['country'] not in countries_list:
            countries_list.append(country['country'])
    for country in institutions_by_country:
        if country['country'] not in countries_list:
            countries_list.append(country['country'])
    for country in communities_by_country:
        if country['country'] not in countries_list:
            countries_list.append(country['country'])

    country_count = len(countries_list)
    
    projects_count = ProjectCreator.objects.select_related('institution', 'community', 'researcher').all().count()


    context = {
            'users_total' : users_total,
            'recent_users_count' : recent_users_count,
            'country_count' : country_count,
            'projects_count': projects_count
        }

    return context

def dataCharts():
    # Colors
    teal_rgb, teal_hex = 'rgba(0, 115, 133, 1)', '#007385'
    light_teal_rgb = 'rgba(43, 138, 153, 1)'
    lighter_teal_rgb = 'rgba(85, 162, 174, 1)'
    orange_rgb, orange_hex = 'rgba(239, 108, 0, 1)', '#EF6C00'
    light_orange_rgb = 'rgba(242, 132, 43, 1)'
    lighter_orange_rgb = 'rgba(244, 157, 85, 1)'
    green_rgb, green_hex = 'rgba(16, 134, 112, 1)', '#108670'
    blue_rgb, blue_hex  = 'rgb(56, 119, 170)', '#3876aa'
    grey_rgb, grey_hex = 'rgba(100, 116, 139, 1)', '#64748B'

    # Registered accounts
    community_count = institution_count = researcher_count = 0
    community_count = Community.objects.count() 
    institution_count = Institution.objects.count() 
    researcher_count = Researcher.objects.count()

    # Notices
    bc_notice_count = tk_notice_count = attr_notice_count = otc_count = disclosure_count = 0
    bc_notice_count = Notice.objects.filter(notice_type="biocultural").count()
    tk_notice_count = Notice.objects.filter(notice_type="traditional_knowledge").count()
    attr_notice_count = Notice.objects.filter(notice_type="attribution_incomplete").count()
    otc_count = OpenToCollaborateNoticeURL.objects.select_related('researcher', 'institution').all().count()
    disclosure_count = bc_notice_count + tk_notice_count + attr_notice_count

    # Labels
    bclabels_customized_count = bclabels_approved_count = bclabels_applied_count = bclabels_total= 0
    tklabels_customized_count = tklabels_approved_count = tklabels_applied_count = tklabels_total = 0
    project_labels_count = project_inactive_count = 0
    bclabels_customized_count = BCLabel.objects.filter(is_approved=False).count()
    tklabels_customized_count = TKLabel.objects.filter(is_approved=False).count()

    bclabels_approved = BCLabel.objects.filter(is_approved=True)
    tklabels_approved = TKLabel.objects.filter(is_approved=True)

    for label in bclabels_approved:
        if BCLabel.objects.filter(unique_id=label.unique_id).exists():
            bclabel = BCLabel.objects.select_related('created_by', 'approved_by').get(unique_id=label.unique_id)
            bclabels_applied = bclabel.project_bclabels.all().count()
        
        if bclabels_applied > 0:
            bclabels_applied_count += 1
        else: 
            bclabels_approved_count += 1

    for label in tklabels_approved:
        if TKLabel.objects.filter(unique_id=label.unique_id).exists():
            tklabel = TKLabel.objects.select_related('created_by', 'approved_by').get(unique_id=label.unique_id)
            tklabels_applied = tklabel.project_tklabels.all().count()
        
        if tklabels_applied > 0:
            tklabels_applied_count += 1
        else: 
            tklabels_approved_count += 1

    bclabels_total = bclabels_customized_count + bclabels_approved_count + bclabels_applied_count
    tklabels_total = tklabels_customized_count + tklabels_approved_count + tklabels_applied_count

    # Projects
    for project in Project.objects.all():
            if project.has_labels():
                project_labels_count += 1
            if project.has_labels() == False and project.has_notice() == False:
                project_inactive_count += 1

    # get last year by months (from today's date)
    start_date = datetime.now(tz=timezone.utc)
    new_users_data = {}
    new_projects_data = {}
    for i in range(1, 13):
        start_month = start_date.month
        month_year = " ".join([calendar.month_name[start_month], str(start_date.year)])
        new_users_data[month_year] = 0
        new_projects_data[month_year] = 0
        start_date -= timedelta(days=calendar.monthrange(start_date.year, start_date.month)[1])

    # add user count based on month/year
    new_users = User.objects.filter(date_joined__gte=datetime.now(tz=timezone.utc) - timedelta(days=365)).annotate(
        month=Extract('date_joined', 'month'),
        year=Extract('date_joined', 'year'),
        ).values('month', 'year').annotate(c=Count('pk')).values('month', 'year', 'c').order_by('year', 'month') 
    
    for user_count in new_users:
        user_month = user_count['month']
        user_month_year = " ".join([calendar.month_name[user_month], str(user_count['year'])])
        new_users_data[user_month_year] = user_count['c']

    new_users_months = list(new_users_data.keys())
    new_users_months.reverse()
    new_users_counts = list(new_users_data.values())
    new_users_counts.reverse()

    # add project count based on month/year
    new_projects = Project.objects.filter(date_added__gte=datetime.now(tz=timezone.utc) - timedelta(days=365)).annotate(
        month=Extract('date_added', 'month'),
        year=Extract('date_added', 'year'),
        ).values('month', 'year').annotate(c=Count('pk')).values('month', 'year', 'c').order_by('year', 'month') 
    
    for project_count in new_projects:
        project_month = project_count['month']
        project_month_year = " ".join([calendar.month_name[project_month], str(project_count['year'])])
        new_projects_data[project_month_year] = project_count['c']

    new_project_months = list(new_projects_data.keys())
    new_project_months.reverse()
    new_project_counts = list(new_projects_data.values())
    new_project_counts.reverse()

    # Pie Chart Data
    accountData = {
                'labels': ['Community', 'Insitution', 'Researcher'],
                'datasets': [{
                    'data': [community_count, institution_count, researcher_count],
                    'backgroundColor': [green_rgb, orange_rgb,teal_rgb],
                    'hoverOffset': 4
                }]
            }
    projectActivityData = {
            'labels': ['Engagement Notice', 'Disclosure Notice', 'Labels Applied', 'No Activity'],
            'datasets': [{
                'data': [otc_count, disclosure_count, project_labels_count, project_inactive_count],
                'backgroundColor': [orange_rgb,teal_rgb,green_rgb,grey_rgb],
                'hoverOffset': 4
            }]
        }
    customizedLabelsData = {
            'labels': ['Customized', 'Approved', 'Applied', 'Customized', 'Approved', 'Applied'],
            'datasets': [
                {
                    'data': [tklabels_customized_count, tklabels_approved_count, tklabels_applied_count, bclabels_customized_count, bclabels_approved_count, bclabels_applied_count],
                    'backgroundColor': [lighter_orange_rgb, light_orange_rgb,orange_rgb, lighter_teal_rgb, light_teal_rgb,teal_rgb],
                    'hoverOffset': 4
                }
            ]
        }
    
    # Line Chart Data
    newUsers = {
            'labels': new_users_months,
            'datasets': [
                {
                'data': new_users_counts,
                'label': 'New Users',
                'fill': 'false',
                'borderColor': orange_rgb,
                'tension':0.2
                },
                {
                'data': new_project_counts,
                'label': 'New Projects',
                'fill': 'false',
                'borderColor': blue_rgb,
                'tension':0.2
                }
            ]
        }
    
    context = {
        'accountData' : accountData,
        'projectActivityData' : projectActivityData,
        'customizedLabelsData' : customizedLabelsData,
        'newUsers' : newUsers,
    }
    
    return context

def user_activity():
    user_activity = []
    user_activity_count =  0

    # Member Invitation Sent
    user_notifications = UserNotification.objects.filter(created__gte=datetime.now(tz=timezone.utc) - timedelta(days=30)).select_related('to_user', 'from_user', 'community', 'institution')
    user_activity_count += user_notifications.count()

    for activity in user_notifications:
        activity_detail = {}
        activity_detail['action_type'] = 'Member Invitation'
        activity_detail['date'] = activity.created
        
        activity_detail['sender_id'] = activity.from_user_id
        activity_detail['sender_first_name'] = getattr(activity.from_user, 'first_name', None)
        activity_detail['sender_last_name'] = getattr(activity.from_user, 'last_name', None)
        activity_detail['sender_username'] = getattr(activity.from_user, 'username', None)

        activity_detail['recipient_id'] = activity.to_user_id
        activity_detail['recipient_first_name'] = getattr(activity.to_user, 'first_name', None)
        activity_detail['recipient_last_name'] = getattr(activity.to_user, 'last_name', None)
        activity_detail['recipient_username'] = getattr(activity.to_user, 'username', None)

        if activity.community_id:
            activity_detail['community_id'] = activity.community_id
            activity_detail['community_name'] = getattr(activity.community, 'community_name', None)
        elif activity.institution_id:
            activity_detail['institution_id'] = activity.institution_id
            activity_detail['institution_name'] = getattr(activity.institution, 'institution_name', None)

        user_activity.append(activity_detail)

    # Sign Up Invitation Sent
    invitation_notifications = SignUpInvitation.objects.filter(date_sent__gte=datetime.now(tz=timezone.utc) - timedelta(days=30)).select_related('sender')
    user_activity_count += invitation_notifications.count()

    for activity in invitation_notifications:
        activity_detail = {}
        activity_detail['action_type'] = 'Sign-Up Invitation'
        activity_detail['date'] = activity.date_sent
        activity_detail['recipient'] = activity.email
        
        activity_detail['sender_id'] = activity.sender_id
        activity_detail['sender_first_name'] = getattr(activity.sender, 'first_name', None)
        activity_detail['sender_last_name'] = getattr(activity.sender, 'last_name', None)
        activity_detail['sender_username'] = getattr(activity.sender, 'username', None)

        user_activity.append(activity_detail)

    # New User Joined
    new_users = User.objects.filter(date_joined__gte=datetime.now(tz=timezone.utc) - timedelta(days=30))
    user_activity_count += new_users.count()

    for activity in new_users:
        activity_detail = {}
        activity_detail['action_type'] = 'New User'
        activity_detail['date'] = activity.date_joined
        
        activity_detail['user_id'] = activity.id
        activity_detail['user_first_name'] = activity.first_name
        activity_detail['user_last_name'] = activity.last_name
        activity_detail['user_username'] = activity.username

        user_activity.append(activity_detail)

    # New Researcher Account Created
    new_researcher_acct = Researcher.objects.filter(date_connected__gte=datetime.now(tz=timezone.utc) - timedelta(days=30)).select_related('user')
    user_activity_count += new_researcher_acct.count()

    for activity in new_researcher_acct:
        activity_detail = {}
        activity_detail['action_type'] = 'New Researcher'
        activity_detail['researcher_id'] = activity.id
        activity_detail['date'] = activity.date_connected
        
        activity_detail['user_id'] = activity.user_id
        activity_detail['user_first_name'] = getattr(activity.user, 'first_name', None)
        activity_detail['user_last_name'] = getattr(activity.user, 'last_name', None)
        activity_detail['user_username'] = getattr(activity.user, 'username', None)

        user_activity.append(activity_detail)

    # New Community Account Created
    new_community_acct = Community.objects.filter(created__gte=datetime.now(tz=timezone.utc) - timedelta(days=30)).select_related('community_creator')
    user_activity_count += new_community_acct.count()

    for activity in new_community_acct:
        activity_detail = {}
        activity_detail['action_type'] = 'New Community'
        activity_detail['community_id'] = activity.id
        activity_detail['community_name'] = activity.community_name
        activity_detail['date'] = activity.created
        
        activity_detail['community_creator_id'] = activity.community_creator_id
        activity_detail['community_creator_first_name'] = getattr(activity.community_creator, 'first_name', None)
        activity_detail['community_creator_last_name'] = getattr(activity.community_creator, 'last_name', None)
        activity_detail['community_creator_username'] = getattr(activity.community_creator, 'username', None)

        user_activity.append(activity_detail)

    # New Institution Account Created
    new_institution_acct = Institution.objects.filter(created__gte=datetime.now(tz=timezone.utc) - timedelta(days=30)).select_related('institution_creator')
    user_activity_count += new_institution_acct.count()

    for activity in new_institution_acct:
        activity_detail = {}
        activity_detail['action_type'] = 'New Institution'
        activity_detail['institution_id'] = activity.id
        activity_detail['institution_name'] = activity.institution_name
        activity_detail['date'] = activity.created
        
        activity_detail['institution_creator_id'] = activity.institution_creator_id
        activity_detail['institution_creator_first_name'] = getattr(activity.institution_creator, 'first_name', None)
        activity_detail['institution_creator_last_name'] = getattr(activity.institution_creator, 'last_name', None)
        activity_detail['institution_creator_username'] = getattr(activity.institution_creator, 'username', None)

        user_activity.append(activity_detail)

    # Sort by date (desc)
    user_activity_sorted = sorted(user_activity, key=lambda k: k['date'])
    user_activity_sorted.reverse()

    context = {
        'user_activity' : user_activity_sorted,
        'user_activity_count' : user_activity_count,
    }
    return context

def project_activity():
    project_activity_count = 0
    project_activity_detail=[]

    # General Project Activity (based on notifications)
    project_activity = ActionNotification.objects.filter(created__gte=datetime.now(tz=timezone.utc) - timedelta(days=30), notification_type='Projects').select_related('sender', 'community', 'institution', 'researcher')
    project_activity_count = project_activity.count()

    for project in project_activity:
        project_detail = {}
        if "A new project was created" in project.title or "Your project has been created" in project.title:
            project_detail['notification_type'] = 'Project Created'
        elif "Edits have been made" in project.title:
            project_detail['notification_type'] = 'Project Edited'
        elif "added as a contributor" in project.title:
            project_detail['notification_type'] = 'Contributor Added'
        elif "has notified you" in project.title:
            project_detail['notification_type'] = 'Community Notified'
            project_detail['sender_account'] = project.title.replace(' has notified you of a Project.', '')
        elif "Labels have been applied" in project.title:
            project_detail['notification_type'] = 'Label(s) Applied'

        project_id = uuid.UUID(project.reference_id)
        project_title = Project.objects.filter(unique_id=project_id).values('title')
        for item in project_title:
            project_detail['project_title'] = item['title']

        project_detail['sender_id'] = project.sender_id
        project_detail['sender_username'] = getattr(project.sender, 'username', None)
        project_detail['sender_first_name'] = getattr(project.sender, 'first_name', None)
        project_detail['sender_last_name'] = getattr(project.sender, 'last_name', None)

        project_detail['community_id'] = project.community_id
        project_detail['community_name'] = getattr(project.community, 'community_name', None)

        project_detail['institution_id'] = project.institution_id
        project_detail['institution_name'] = getattr(project.institution, 'institution_name', None)

        project_detail['researcher_id'] = project.researcher_id
        project_detail['researcher_username'] = getattr(getattr(project.researcher, 'user', None), 'username', None)
        project_detail['researcher_first_name'] = getattr(getattr(project.researcher, 'user', None), 'first_name', None)
        project_detail['researcher_last_name'] = getattr(getattr(project.researcher, 'user', None), 'last_name', None)

        project_detail['reference_id'] = project.reference_id
        project_detail['date'] = project.created

        project_activity_detail.append(project_detail)

    # Notice added to Project
    for project in project_activity_detail:
        if project['notification_type'] == 'Project Created' and project['community_id'] is None:
            project_activity_count += 1
            project_detail = {}
            project_detail['notification_type'] = 'Disclosure Notice(s) Added'
            project_detail['project_title'] = project['project_title']

            project_detail['sender_id'] = project['sender_id']
            project_detail['sender_username'] = project['sender_username']
            project_detail['sender_first_name'] = project['sender_first_name']
            project_detail['sender_last_name'] = project['sender_last_name']

            project_detail['institution_id'] = project['institution_id']
            project_detail['institution_name'] = project['institution_name']

            project_detail['researcher_id'] = project['researcher_id']
            project_detail['researcher_username'] = project['researcher_username']
            project_detail['researcher_first_name'] = project['researcher_first_name']
            project_detail['researcher_last_name'] = project['researcher_last_name']

            project_detail['reference_id'] = project['reference_id']
            project_detail['date'] = project['date']

            project_activity_detail.append(project_detail)

    # OTC Notice Added
    otc_added = OpenToCollaborateNoticeURL.objects.filter(added__gte=datetime.now(tz=timezone.utc) - timedelta(days=30)).select_related('institution', 'researcher')
    project_activity_count += otc_added.count()

    for project in otc_added:
        project_detail = {}

        project_detail['notification_type'] = 'Engagement Notice Added'
        project_detail['project_title'] = project.name
        project_detail['project_link'] = project.url

        project_detail['institution_id'] = project.institution_id
        project_detail['institution_name'] = getattr(project.institution, 'institution_name', None)

        project_detail['researcher_id'] = project.researcher_id
        project_detail['researcher_username'] = getattr(getattr(project.researcher, 'user', None), 'username', None)
        project_detail['researcher_first_name'] = getattr(getattr(project.researcher, 'user', None), 'first_name', None)
        project_detail['researcher_last_name'] = getattr(getattr(project.researcher, 'user', None), 'last_name', None)

        project_detail['date'] = project.added

        project_activity_detail.append(project_detail)
        
    # Sort by date (desc)
    project_activity_sorted = sorted(project_activity_detail, key=lambda k: k['date'])
    project_activity_sorted.reverse()

    context = {
        'project_activity_detail' : project_activity_sorted,
        'project_activity_count' : project_activity_count,
    }

    return context

def inactive_users():
    inactive_user_data = User.objects.filter(is_active=False, date_joined__lte=datetime.now(tz=timezone.utc) - timedelta(days=30)).annotate(days_count=datetime.now(tz=timezone.utc) - F('date_joined')).values('id', 'username', 'days_count')

    researcher_created_projects = ProjectCreator.objects.filter(researcher__isnull=False).values_list('researcher_id')
    inactive_researchers = Researcher.objects.exclude(id__in=researcher_created_projects).filter(date_connected__lte=datetime.now(tz=timezone.utc) - timedelta(days=90)).annotate(days_count=datetime.now(tz=timezone.utc) - F('date_connected')).values('id', 'user__username', 'user__first_name', 'user__last_name', 'days_count')

    unconfirmed_institutions = Institution.objects.filter(is_approved=False, created__lte=datetime.now(tz=timezone.utc) - timedelta(days=90)).annotate(days_count=datetime.now(tz=timezone.utc) - F('created')).values('id', 'institution_name', 'days_count')

    unconfirmed_communities = Community.objects.filter(is_approved=False, created__lte=datetime.now(tz=timezone.utc) - timedelta(days=90)).annotate(days_count=datetime.now(tz=timezone.utc) - F('created')).values('id', 'community_name', 'days_count')

    # Sort by date (desc)
    inactive_data = list(itertools.chain(inactive_user_data, inactive_researchers, unconfirmed_institutions, unconfirmed_communities))
    inactive_data_sorted = sorted(inactive_data, key=lambda k: k['days_count'])
    inactive_data_count = len(inactive_data)

    context = {
        'inactive_user_data' : inactive_user_data,
        'inactive_researchers' : inactive_researchers,
        'unconfirmed_institutions' : unconfirmed_institutions,
        'unconfirmed_communities' : unconfirmed_communities,

        'inactive_data_sorted' : inactive_data_sorted,
        'inactive_data_count' : inactive_data_count
    }

    return context

# ACCOUNTS ADMIN
class UserAdminCustom(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name',)

class SignUpInvitationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'email', 'date_sent')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'affiliation', 'is_researcher')
    readonly_fields = ('api_key',)

admin_site.register(Profile, ProfileAdmin)
admin_site.register(UserAffiliation)
admin_site.register(SignUpInvitation, SignUpInvitationAdmin)

# admin_site.unregister(User)
admin_site.register(User, UserAdminCustom)

# API KEYS ADMIN
admin_site.register(APIKey, APIKeyModelAdmin)

# AUTH ADMIN
class MyGroupAdmin(GroupAdmin):
    # Add customizations here, if needed
    pass

admin_site.register(Group, MyGroupAdmin)

# BCLABELS ADMIN
class BCLabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'community', 'created_by', 'language_tag', 'language', 'is_approved', 'created',)
    readonly_fields = ('unique_id', 'created', 'version',)
    search_fields = ('name', 'community__community_name', 'created_by__username',)

admin_site.register(BCLabel, BCLabelAdmin)

# COMMUNITIES ADMIN
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('community_name', 'community_creator', 'contact_name', 'contact_email', 'is_approved', 'created', 'country')
    search_fields = ('community_name', 'contact_name', 'contact_email',)
    readonly_fields = ('native_land_slug',)

class JoinRequestAdmin(admin.ModelAdmin):
    list_display = ('community', 'institution', 'user_from', 'user_to', 'status', 'date_sent')
    search_fields = ('community__community_name', 'institution__institution_name', 'user_from__username',)

class InviteMemberAdmin(admin.ModelAdmin):
    list_display = ('community', 'institution', 'sender', 'receiver', 'role', 'status', 'created')
    search_fields = ('community__community_name', 'institution__institution_name', 'sender__username', 'receiver__username',)

admin_site.register(Community, CommunityAdmin)
admin_site.register(InviteMember, InviteMemberAdmin)
admin_site.register(JoinRequest, JoinRequestAdmin)

# HELPERS ADMIN
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('project', 'notice_type', 'researcher', 'institution', 'created', 'archived' )
    search_fields = ('project__title', 'notice_type', 'researcher__user__username', 'institution__institution_name')

class OpenToCollaborateNoticeURLAdmin(admin.ModelAdmin):
    list_display = ('institution', 'researcher', 'name', 'url', 'added')
    search_fields = ('institution__institution_name', 'researcher__user__username', 'name', 'url')

class LabelTranslationAdmin(admin.ModelAdmin):
    list_display = ('translated_name', 'language', 'language_tag', 'translated_text', )

class EntitiesNotifiedAdmin(admin.ModelAdmin):
    list_display = ('project',)
    search_fields = ('project__title',)

class LabelVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'bclabel', 'tklabel', 'created', 'is_approved')
    readonly_fields = ('bclabel', 'tklabel', 'version', 'version_text', 'created_by', 'approved_by', 'created',)

class LabelTranslationVersionAdmin(admin.ModelAdmin):
    list_display = ('version_instance', 'translated_name', 'language', 'created')
    readonly_fields = ('version_instance', 'translated_name', 'language', 'language_tag', 'translated_text', 'created',)

class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('project', 'community', 'seen', 'status')
    search_fields = ('project__title', 'community__community_name')

# class ProjectCommentAdmin(admin.ModelAdmin):
#     list_display = ('project', 'sender', 'community', 'sender_affiliation', 'message', 'created')
#     search_fields = ('project',)

# class LabelNoteAdmin(admin.ModelAdmin):
#     list_display = ('bclabel', 'tklabel', 'sender',)

# admin_site.register(ProjectComment, ProjectCommentAdmin)
# admin_site.register(LabelNote, LabelNoteAdmin)
admin_site.register(ProjectStatus, ProjectStatusAdmin)
admin_site.register(Notice, NoticeAdmin)
admin_site.register(LabelVersion, LabelVersionAdmin)
admin_site.register(LabelTranslationVersion, LabelTranslationVersionAdmin)
admin_site.register(LabelTranslation, LabelTranslationAdmin)
admin_site.register(EntitiesNotified, EntitiesNotifiedAdmin)
admin_site.register(OpenToCollaborateNoticeURL, OpenToCollaborateNoticeURLAdmin)

# INSTITUTIONS ADMIN
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('institution_name', 'institution_creator', 'contact_name', 'contact_email', 'is_approved', 'is_ror', 'created', 'country')
    search_fields = ('institution_name', 'institution_creator__username', 'contact_name', 'contact_email',)

admin_site.register(Institution, InstitutionAdmin)

# NOTIFICAITONS ADMIN
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'community', 'notification_type', 'title', 'reference_id', 'created')

class ActionNotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'community', 'institution', 'researcher', 'notification_type', 'title', 'created')

admin_site.register(UserNotification, UserNotificationAdmin)
admin_site.register(ActionNotification, ActionNotificationAdmin)

# PROJECTS ADMIN
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_creator', 'project_contact', 'project_contact_email', 'project_privacy', 'project_page', 'date_added', 'unique_id')
    readonly_fields = ('unique_id', 'project_page')
    search_fields = ('title', 'unique_id', 'project_creator__username', 'project_contact', 'project_contact_email',)

class ProjectContributorsAdmin(admin.ModelAdmin):
    list_display = ('project',)
    search_fields = ('project__title',)

class ProjectPersonAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'email')

class ProjectCreatorAdmin(admin.ModelAdmin):
    list_display = ('project', 'community', 'institution', 'researcher')
    search_fields = ('project__title',)

class ProjectActivityAdmin(admin.ModelAdmin):
    list_display = ('project', 'date', 'activity')    
    readonly_fields = ('project', 'date', 'activity')
    search_fields = ('project__title',)

class ProjectArchivedAdmin(admin.ModelAdmin):
    list_display = ('project_uuid', 'archived', 'community_id', 'institution_id', 'researcher_id')

class ProjectNoteAdmin(admin.ModelAdmin):
    list_display = ('project', 'community')

admin_site.register(Project, ProjectAdmin)
admin_site.register(ProjectContributors, ProjectContributorsAdmin)
admin_site.register(ProjectPerson, ProjectPersonAdmin)
admin_site.register(ProjectCreator, ProjectCreatorAdmin)
admin_site.register(ProjectActivity, ProjectActivityAdmin)
admin_site.register(ProjectArchived, ProjectArchivedAdmin)
admin_site.register(ProjectNote, ProjectNoteAdmin)

# RESEARCHERS ADMIN
class ResearcherAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_email', 'orcid', 'primary_institution', 'date_connected')
    search_fields = ('contact_email', 'user__username', 'orcid', 'primary_institution', 'date_connected')
    readonly_fields = ('orcid_auth_token',)

admin_site.register(Researcher, ResearcherAdmin)

# TKLABELS ADMIN
class TKLabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'community', 'created_by', 'language_tag', 'language', 'is_approved', 'created')
    readonly_fields = ('unique_id', 'created', 'version',)
    search_fields = ('name', 'community__community_name', 'created_by__username',)

admin_site.register(TKLabel, TKLabelAdmin)