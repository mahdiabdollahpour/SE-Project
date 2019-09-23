import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from group.models import Group


class MessageQuerySet(models.query.QuerySet):

    def get_conversation(self, sender, recipient):
        qs_one = self.filter(sender=sender, recipient=recipient)
        qs_two = self.filter(sender=recipient, recipient=sender)
        return qs_one.union(qs_two).order_by('timestamp')

    def mark_conversation_as_read(self, sender, recipient):
        qs = self.filter(sender=sender, recipient=recipient)
        return qs.update(unread=False)


class Message(models.Model):
    uuid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sender',
        verbose_name=_("Sender"), null=False, on_delete=models.DO_NOTHING)

    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000, null=True)
    file = models.FileField(upload_to='message_files/', null=True)
    # format
    visited = models.BooleanField(default=False, db_index=True)
    objects = MessageQuerySet.as_manager()

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ("-timestamp",)

    def __str__(self):
        return self.message

    def mark_as_visited(self):
        """Method to mark a message as read."""
        if self.visited:
            self.visited = True
            self.save()

    @staticmethod
    def send_message(sender, recipient, message, type):
        new_message = Message.objects.create(
            sender=sender,
            recipient=recipient,
            message=message
        )

        channel_layer = get_channel_layer()
        payload = {
            'type': 'consume_message',
            'key': 'message',
            'message_id': new_message.uuid_id,
            'sender': sender,
            'recipient': recipient
        }
        async_to_sync(channel_layer.group_send)(str("user-{}".format(recipient.id)), payload)
        return new_message


class ChatMessage(models.Model):
    message = models.ForeignKey(Message, related_name='message',
                                verbose_name=_("Message"), null=False, on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='receiver',
        verbose_name=_("Recipient"), null=False, on_delete=models.DO_NOTHING)


class GroupMessage(models.Model):
    message = models.ForeignKey(Message, related_name='message',
                                verbose_name=_("Message"), null=False, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, related_name='group_id',
                                 verbose_name=_("Group_id"), null=False, on_delete=models.CASCADE)
