from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from communities.models import InviteMember
from notifications.models import UserNotification
from localcontexts.utils import dev_prod_or_local
from .downloads import download_otc_notice
import requests

def restricted_view(request, exception=None):
    return render(request, '403.html', status=403)

@login_required(login_url='login')
def delete_member_invite(request, pk):
    invite = InviteMember.objects.get(id=pk)
    
    # Delete relevant UserNotification
    if UserNotification.objects.filter(to_user=invite.receiver, from_user=invite.sender, notification_type='invitation', reference_id=pk).exists():
        notification = UserNotification.objects.get(to_user=invite.receiver, notification_type='invitation', reference_id=pk)
        notification.delete()

    invite.delete()

    if '/communities/' in request.META.get('HTTP_REFERER'):
        return redirect('member-requests', invite.community.id)
    else:
        return redirect('institution-member-requests', invite.institution.id)
    

@login_required(login_url='login')
def download_open_collaborate_notice(request, perm):
    # perm will be a 1 or 0
    has_permission = bool(perm)
    if dev_prod_or_local(request.get_host()) == 'DEV' or not has_permission:
        return redirect('restricted')
    else:
        return download_otc_notice()

@login_required(login_url='login')
def download_community_support_letter(request):
    try:
        url = 'https://storage.googleapis.com/anth-ja77-local-contexts-8985.appspot.com/agreements/Local%20Contexts%20Community%20Support%20Letter%20Template.docx'
        response = requests.get(url)

        if response.status_code == 200:
            file_content = response.content
            response = HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename="LC_Community_Support_Letter_Template.docx"'
            return response
    except:
        raise Http404()

@login_required(login_url='login')
def download_institution_support_letter(request):
    try:
        url = 'https://storage.googleapis.com/anth-ja77-local-contexts-8985.appspot.com/agreements/Local%20Contexts%20Institution%20Information%20and%20Support%20Letter%20Template.docx'
        response = requests.get(url)

        if response.status_code == 200:
            file_content = response.content
            response = HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename="LC_Institution_Support_Letter_Template.docx"'
            return response
    except:
        raise Http404()