from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver, Signal
from django.contrib.auth.models import User, Group
from communities.models import *
from bclabels.models import BCNotice
from .models import *
from .utils import *

# Sends welcome notification to user that just registered
@receiver(post_save, sender=User)
def create_welcome_message(sender, instance, created, **kwargs):
    if created:
        UserNotification.objects.create(to_user=instance, title="Welcome", message="You have joined", notification_type="welcome")

# When the instance of invite member form is saved, send target user a notification
@receiver(post_save, sender=InviteMember)
def send_community_invite(sender, instance, created, **kwargs):
    if instance.status == 'sent':
        sender_ = instance.sender
        receiver_ = instance.receiver
        role = instance.role
        community = instance.community
        ref = instance.id
        msg = instance.message

        name = check_full_name(sender_)

        title = "You've been invited by " + str(name) + " to join " + str(community) + "!"

        if msg:
            message = msg
        else:
            message= "Join our Community! " + str(community) + " with the role of " + str(role)

        UserNotification.objects.create(to_user=receiver_, title=title, message=message, notification_type="invitation", community=community, reference_id=ref, role=role)

# When an invitation to a community is accepted, send target a notification
@receiver(post_save, sender=InviteMember)
def accept_community_invite(sender, instance, **kwargs):
    if instance.status == 'accepted':
        sender_ = instance.sender
        receiver_ = instance.receiver
        role = instance.role
        community = instance.community
        ref = instance.id

        # Lets user know they are now a member
        title = "You are now a member of " + str(community) + "!"
        message = "Congrats"
        
        UserNotification.objects.create(to_user=receiver_, from_user=sender_, title=title, message=message, notification_type="accept", community=community, reference_id=ref)

        # Lets sender know their invitation was accepted
        title2 = str(check_full_name(receiver_)) + " has accepted your invitation to join " + str(community) + "!"
        message2 = "Woohoo"
        
        UserNotification.objects.create(to_user=sender_, from_user=receiver_, title=title2, message=message2, notification_type="accept", community=community, reference_id=ref)

        instance.delete() # Deletes the invitation after it has been accepted

# Send notification when user wishes to join a community
@receiver(post_save, sender=CommunityJoinRequest)
def send_user_join_request(sender, instance, created, **kwargs):
    if created:
        receiver_ = instance.user_to
        sender_ = instance.user_from
        community = instance.target_community
        ref = instance.id

        name = check_full_name(sender_)

        title = str(name) + " wishes to join " + str(community)
        message = "You can add " + str(name) + " to " + str(community)

        UserNotification.objects.create(to_user=receiver_, from_user=sender_, title=title, message=message, notification_type="request", community=community, reference_id=ref)

# Send notification when a user's join request has been accepted and they are now part of a community.
@receiver(post_save, sender=CommunityJoinRequest)
def accept_user_join_request(sender, instance, created, **kwargs):
    if instance.status == 'accepted':
        receiver_ = instance.user_to
        sender_ = instance.user_from
        community = instance.target_community
        ref = instance.id

        # Message to user requesting to join after request has been approved.
        title = " You are now a member of " + str(community)
        message = "Your role is " + str(instance.role)

        UserNotification.objects.create(to_user=sender_, from_user=receiver_, title=title, message=message, notification_type="accept", community=community, reference_id=ref)

        # Message to user accepting the join request letting them know user is now a community member.
        title2 = str(check_full_name(sender_)) + " is now a member of " + str(community)
        message2 = "Woot"

        UserNotification.objects.create(to_user=receiver_, from_user=sender_, title=title2, message=message2, notification_type="accept", community=community, reference_id=ref)
        instance.delete() # Deletes the request when it has been accepted

# Sends Site admin notifiation with request to create community
#TODO: Test this when there is more than one site admin
@receiver(post_save, sender=Community)
def community_application(sender, instance, created, **kwargs):
    creator = instance.community_creator
    # site_admin = User.objects.get(username="dianalovette")
    site_admins = User.objects.filter(groups__name='Site Administrator')

    name = check_full_name(creator)

    title = str(name) + " wants to create a community: " + str(instance.community_name)
    message = "Community application."

    if created:
        for admin in site_admins:
            UserNotification.objects.create(to_user=admin, from_user=creator, title=title, message=message, notification_type="create", community=instance)

#TODO: Figure out the signal for sending a community a notification when a BC Label is created.
# @receiver(m2m_changed, sender=BCNotice.communities.through)
# def notice_placed(sender, instance, created, **kwargs):
#     if created:
        # Get all communities of the notice
        
        # Send a notification to each of them
        # CommunityNotification.objects.create(community=community.id, title="A notice was placed", notification_type="requests")

