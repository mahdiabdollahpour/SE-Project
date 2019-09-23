from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# def send_mail(to, template, context):
#     html_content = render_to_string('accounts/emails/{t}.html'.format(t=template), context)
#     text_content = render_to_string('accounts/emails/{t}.txt'.format(t=template), context)
#
#     msg = EmailMultiAlternatives(context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()


# def send_activation_email(request, email, code):
#     context = {
#         'subject': _('Profile activation'),
#         'uri': request.build_absolute_uri(reverse('accounts:activate', kwargs={'code': code})),
#     }
#
#     send_mail(email, 'activate_profile', context)

def send_activation_code(request, phoneNumber, code):
    pass


# def send_activation_change_email(request, email, code):
#     context = {
#         'subject': _('Change email'),
#         'uri': request.build_absolute_uri(reverse('accounts:change_email_activation', kwargs={'code': code})),
#     }
#
#     send_mail(email, 'change_email', context)


# def send_reset_password_email(request, email, token, uid):
#     context = {
#         'subject': _('Restore password'),
#         'uri': request.build_absolute_uri(
#             reverse('accounts:restore_password_confirm', kwargs={'uidb64': uid, 'token': token})),
#     }
#
#     send_mail(email, 'restore_password_email', context)

def send_password(request, password, phoneNumber):
    pass


def send_username(phoneNumber, username):
    # context = {
    #     'subject': _('Your username'),
    #     'username': username,
    # }
    #
    # send_mail(email, 'forgotten_username', context)
    pass


def expire_activation_code(code):
    pass


def is_activation_code_expired(code):
    pass


def delete_activation_code(code):
    pass


def add_user_to_online_list(user):
    pass


def delete_user_from_online_list(user):
    pass


def contact_list_contains_phone_number(user, phone_number):
    pass


def user_phone_number_equals_contact_phone_number(user, phone_number):
    pass


def phone_number_exists(phone_number):
    pass


def add_user_to_contact_list(user_1, user_2):
    pass


def update_contact_list(user_1, user_2, new_phone_number):
    pass


def user_exists_or_not(user):
    pass


def user_1_blocked_user_2(user_1, user_2):
    pass


def user_1_equals_user_2(user_1, user_2):
    pass


def is_user_in_group(user, group):
    pass


def is_user_in_team(user, team):
    pass


def add_user_to_group(user, group):
    pass


def add_user_to_team(user, team):
    pass


def is_user_admin_of_group(user, group):
    pass


def is_user_admin_of_team(user, team):
    pass


def is_user_coleader_of_group(user, group):
    pass


def is_user_coleader_of_team(user, team):
    pass


def make_user_coleader_of_group(user, group):
    pass


def make_user_coleader_of_team(user, team):
    pass


def is_user_assigned_task(user, task):
    pass
