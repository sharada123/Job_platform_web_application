from django.db.models.signals import post_save

from django.dispatch import receiver
from .models import CustomUser,Profile

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)  # Create profile if missing
    else:
        instance.profile.save()
