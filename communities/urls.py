from django.urls import path
from . import views

urlpatterns = [
    path('connect-community/', views.connect_community, name="connect-community"),
    path('create-community/', views.create_community, name="create-community"),
    path('community-registry/', views.community_registry, name="community-registry"),

    path('community/dashboard/<str:pk>/', views.community_dashboard, name="community-dashboard"),
    path('community/dashboard/update/<str:pk>/', views.update_community, name="update-community"),

    path('community/members/<str:pk>/', views.community_members, name="members"),
    path('community/members/add/<str:pk>/', views.add_member, name="add-member"),
    
    path('community/activity/<str:pk>/', views.community_activity, name="community-activity"),

    path('community/labels/<str:pk>/', views.community_labels, name="community-labels"),
    path('community/labels/select/<str:pk>/', views.select_label, name="select-label"),

    path('community/labels/<str:pk>/<str:label_id>/', views.approve_bclabel, name="approve-label"),
    path('community/labels/tk/<str:pk>/<str:label_id>/', views.approve_tklabel, name="approve-tklabel"),

    path('community/labels/customise/bc/<str:pk>/<str:label_type>', views.customise_bclabel, name="customise-bclabel"),
    path('community/labels/customise/tk/<str:pk>/<str:label_type>', views.customise_tklabel, name="customise-tklabel"),
    
    path('community/activity/notice/add/<str:pk>/<str:notice_id>', views.apply_notice_labels, name="community-add-labels"),
    path('community/projects/add/<str:pk>/<str:project_id>', views.apply_project_labels, name="apply-project-labels"),

    path('community/projects/<str:pk>/', views.projects, name="community-projects"),
    path('community/projects/create-project/<str:pk>/', views.create_project, name="create-project"),

    path('community/relationships/<str:pk>/', views.community_relationships, name="community-relationships"),

    path('community/restricted/<str:pk>/', views.restricted_view, name="restricted"),
]