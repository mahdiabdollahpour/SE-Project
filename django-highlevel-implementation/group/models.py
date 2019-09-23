import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class GroupQuerySet(models.query.QuerySet):
    pass


class Group(models.Model):
    uuid_id = models.UUIDField(_('gp_id'),
                               primary_key=True, default=uuid.uuid4, editable=False)
    link = models.UUIDField(_('gp_link'),
                            primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Group's name"), max_length=255)
    image = models.ImageField(
        _("Group's picture"), upload_to='group_pics/', null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)
    link_visibility = models.BooleanField(default=True)

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='admin',
        verbose_name=_("Admin"), null=False, on_delete=models.DO_NOTHING)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uuid_id
