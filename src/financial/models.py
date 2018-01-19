import qrcode
import io

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

class MomoData(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='momo')
    momo_number = models.CharField(max_length=12)
    momo_name = models.CharField(max_length=50)
    changeCount = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
   
class Transaction(models.Model):

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction')
    to          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    image_proof = models.ImageField(upload_to='proofs', blank=True, null=True)
    text_proof  = models.TextField(blank=True, null=True)
    amount      = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    level       = models.IntegerField(default=0)
    state       = models.CharField(max_length=10, default="pending")
    timestamp   = models.DateTimeField(auto_now_add=True, auto_now=False)


class Missed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='missed')
    was_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='was_to_user')
    missed_to = models.CharField(max_length=30)
    trans_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=4, decimal_places=3)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


class Report(models.Model):
    by =  models.ForeignKey(User, related_name='report_by')
    against = models.ForeignKey(User, related_name='report_against')
    trans_id = models.ForeignKey(Transaction, related_name='report')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
