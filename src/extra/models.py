from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models


class Action(models.Model):
    user = models.ForeignKey(User, related_name='actions', db_index=True)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj')
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    additional = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

class Notif_Count(models.Model):
    target =  models.ForeignKey(User, related_name='notification', db_index=True)
    count = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.target.username
