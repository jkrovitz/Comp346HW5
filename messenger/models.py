from __future__ import unicode_literals
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Message(models.Model):
    text = models.TextField()
    sent = models.BooleanField()
    date = models.DateField(default=timezone.now)
    sender = models.ForeignKey(User, related_name='sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received', on_delete=models.CASCADE)
