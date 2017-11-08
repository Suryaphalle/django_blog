# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from blog.utils import random_string_generater
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User)
    email_confirmed = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=100, blank=True, null=True)
    acitvated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.user, self.acitvated)

    def __unicode__(self):
        return '{} {}'.format(self.user, self.acitvated)

@receiver(post_save,sender=User)
def save_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()