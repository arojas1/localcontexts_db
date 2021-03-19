from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Institution
from researchers.models import Researcher
from projects.models import Project
from .forms import CreateInstitutionForm, UpdateInstitutionForm

@login_required(login_url='login')
def connect_institution(request):
    return render(request, 'institutions/connect-institution.html')

@login_required(login_url='login')
def create_institution(request):
    if request.method == 'POST':
        form = CreateInstitutionForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.institution_creator = request.user
            data.save()
            return redirect('dashboard')
    else:
        form = CreateInstitutionForm()
        return render(request, 'institutions/create-institution.html', {'form': form})

@login_required(login_url='login')
def institution_registry(request):
    institutions = Institution.objects.all()
    return render(request, 'institutions/institution-registry.html', {'institutions': institutions})

# Dashboard / Activity
@login_required(login_url='login')
def institution_dashboard(request, pk):
    institution = Institution.objects.get(id=pk)
    return render(request, 'institutions/dashboard.html', {'institution': institution})

# Update institution
@login_required(login_url='login')
def update_institution(request, pk):
    institution = Institution.objects.get(id=pk)
    return render(request, 'institutions/update-institution.html', {'institution': institution})

# Requests (Notices)
@login_required(login_url='login')
def institution_requests(request, pk):
    institution = Institution.objects.get(id=pk)
    return render(request, 'institutions/requests.html', {'institution': institution})

# Projects
@login_required(login_url='login')
def institution_projects(request, pk):
    institution = Institution.objects.get(id=pk)
    return render(request, 'institutions/projects.html', {'institution': institution})

# Create Projects
@login_required(login_url='login')
def create_project(request, pk):
    institution = Institution.objects.get(id=pk)
    return render(request, 'institutions/create-project.html', {'institution': institution})
