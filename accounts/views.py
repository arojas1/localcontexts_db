from django.shortcuts import render, redirect
from django.contrib import messages, auth

from django.contrib.auth.models import User
from django.views.generic import View
from communities.views import connect_community
from .models import Profile
from .forms import RegistrationForm, UserCreateProfileForm, UserUpdateForm, ProfileUpdateForm

# Imports for sending emails
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.contrib.sites.shortcuts import get_current_site


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Remember the current location
            current_site=get_current_site(request)
            template = render_to_string('snippets/activate.html', 
            {
                'user': user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })

            to_email = form.cleaned_data.get('email')

            email_contents = EmailMessage(
                #Email subject
                'Activate Your Account',
                #Body of the email
                template,
                #Sender
                settings.EMAIL_HOST_USER,
                #Recipient, in list to send to multiple addresses at a time.
                [to_email]
            )
            email_contents.fail_silently=False
            email_contents.send()
            return redirect('verify')
    else: 
        form = RegistrationForm()
    
    return render(request, "accounts/register.html", { "form" : form })

def login(request):
    if request.method == 'POST':
        # email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        # If user is found, log in the user.
        if user is not None:
            if not user.last_login:
                auth.login(request, user)
                return redirect('create-profile')
            else:
                auth.login(request, user)
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, "accounts/login.html")

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None

        if user is not None and generate_token.check_token(user, token):
            user.is_active=True
            user.save()
            messages.add_message(request, messages.INFO, 'Account activation successful. You may now log in.')
            return redirect('login')
        return render(request, 'snippets/activate-failed.html', status=401)

def verify(request):
    return render(request, 'accounts/verify.html')
    
@login_required
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')

@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")

@login_required
def create_profile(request):
    if request.method == 'POST':
        #TODO: add classes to input instances so it's easier to style
        user_form = UserCreateProfileForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # Redirects based on what is selected in the dropdown
            if request.POST.get('registration_reason') == 'community':
                return redirect('connect-community')
            elif request.POST.get('registration_reason') == 'institution':
                return redirect('connect-institution')
            elif request.POST.get('registration_reason') == 'researcher':
                return redirect('connect-researcher')

            return redirect('dashboard')
    else:
        user_form = UserCreateProfileForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/create-profile.html', context)

@login_required
def update_profile(request):
    #TODO: add a password reset form
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated!')
            return redirect('update-profile')
        else:
            messages.add_message(request, messages.ERROR, 'Form was not validated')
            return redirect('update-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/update-profile.html', context)