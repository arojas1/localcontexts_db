from django.urls import path
from . import views

urlpatterns = [
    path('connect-institution/', views.connect_institution, name="connect-institution"),
    path('create-institution/', views.create_institution, name="create-institution"),
    path('institution-registry/', views.institution_registry, name="institution-registry"),

    path('institution/<str:pk>/', views.institution_dashboard, name="institution-dashboard"),
    path('institution/update/<str:pk>/', views.update_institution, name="update-institution"),

    path('institution/requests/<str:pk>/', views.institution_requests, name="institution-requests"),

    path('institution/projects/<str:pk>/', views.institution_projects, name="institution-projects"),
    path('institution/create-project/<str:pk>/', views.create_project, name="inst-create-project"),
]