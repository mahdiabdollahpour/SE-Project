from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from group.models import Group
from team.models import Team, Task


class User(AbstractUser):
    name = models.CharField(_("User's name"), blank=True, max_length=255)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    image = models.ImageField(
        _('Profile picture'), upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username

    def get_profile_name(self):
        if self.name:
            return self.name

        return self.username


class Activation(models.Model):
    phone = PhoneNumberField(primary_key=True, null=False, blank=False, unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        # validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)


class BlockedMember(models.Model):
    blocker = models.ForeignKey(
        settings.AUTH_USER_MODEL, primary_key=True, null=False, related_name="blocker",
        on_delete=models.CASCADE)
    blocked = models.ForeignKey(
        settings.AUTH_USER_MODEL, primary_key=True, null=False, related_name="blocked",
        on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL, primary_key=True, null=False, related_name="person",
        on_delete=models.CASCADE)
    contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, primary_key=True, null=False, related_name="contact",
        on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class GroupMember(models.Model):
    group_id = models.ForeignKey(Group, related_name='group_id',
                                 verbose_name=_("Group_id"), null=False, on_delete=models.CASCADE)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='member',
        verbose_name=_("Member"), null=False, on_delete=models.CASCADE)
    is_coleader = models.BooleanField(default=False, db_index=True)


class TeamMember(models.Model):
    team_id = models.ForeignKey(Team, related_name='team_id',
                                verbose_name=_("Team_id"), null=False, on_delete=models.CASCADE)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='member',
        verbose_name=_("Member"), null=False, on_delete=models.CASCADE)
    is_coleader = models.BooleanField(default=False, db_index=True)


class TaskMember(models.Model):
    task = models.ForeignKey(Task, related_name='task',
                             verbose_name=_("Task"), null=False, on_delete=models.CASCADE)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='member',
        verbose_name=_("Member"), null=False, on_delete=models.CASCADE)
