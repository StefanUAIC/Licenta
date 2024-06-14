from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import Notification
from .models import Post


@receiver(post_save, sender=Post)
def post_status_update(sender, instance, **kwargs):
    if instance.status == 'REJECTED':
        message = f'Your post "{instance.title}" has been rejected.'
        Notification.objects.create(user=instance.author, message=message)
    elif instance.status == 'ACCEPTED':
        message = f'Your post "{instance.title}" has been accepted.'
        Notification.objects.create(user=instance.author, message=message)
