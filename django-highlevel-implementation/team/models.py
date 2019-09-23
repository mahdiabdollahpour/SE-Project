import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class TeamQuerySet(models.query.QuerySet):
    pass


class ProjectQuerySet(models.query.QuerySet):
    pass


class TaskQuerySet(models.query.QuerySet):
    pass


class Team(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Team's name"), max_length=255)
    image = models.ImageField(
        _("Team's picture"), upload_to='team_pics/', null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='admin',
        verbose_name=_("Admin"), null=False, on_delete=models.DO_NOTHING)


class Project(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team_id = models.ForeignKey(Team, related_name='team', verbose_name='Team', null=False,
                                on_delete=models.CASCADE)
    name = models.CharField(_("Project's name"), max_length=255)
    image = models.ImageField(
        _("Projects's picture"), upload_to='project_pics/', null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)


class Task(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.ForeignKey(Project, related_name='project', verbose_name='Project', null=False,
                                   on_delete=models.CASCADE)

    name = models.CharField(_("Task's name"), max_length=255)
    image = models.ImageField(
        _("Task's picture"), upload_to='task_pics/', null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)
    deadline = models.DateTimeField()
