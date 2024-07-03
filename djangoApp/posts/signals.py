from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import Notification
from .models import Post


@receiver(post_save, sender=Post)
def post_status_update(sender, instance, **kwargs):
    if instance.status == 'REJECTED':
        message = f'Postarea ta "{instance.title}" a fost respinsă.'
        Notification.objects.create(user=instance.author, message=message)
    elif instance.status == 'ACCEPTED':
        message = f'Postarea ta "{instance.title}" a fost acceptată.'
        Notification.objects.create(user=instance.author, message=message)
