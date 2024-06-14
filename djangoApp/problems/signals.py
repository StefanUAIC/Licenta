from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import Notification
from .models import Problem


@receiver(post_save, sender=Problem)
def post_status_update(sender, instance, **kwargs):
    print(f'instance.status: {instance.status}')
    if instance.status == 'REJECTED':
        message = f'Your problem "{instance.title}" has been rejected.'
        Notification.objects.create(user=instance.created_by, message=message)
    elif instance.status == 'ACCEPTED':
        message = f'Your problem "{instance.title}" has been accepted.'
        Notification.objects.create(user=instance.created_by, message=message)
