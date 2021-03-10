from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=User)
def profile_creation(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(instance)
