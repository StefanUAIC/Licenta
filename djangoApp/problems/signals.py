from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import Notification
from .models import Problem


@receiver(post_save, sender=Problem)
def post_status_update(sender, instance, **kwargs):
    print(f'instance.status: {instance.status}')
    if instance.status == 'REJECTED':
        message = f'Problema ta "{instance.title}" a fost respinsă.'
        Notification.objects.create(user=instance.created_by, message=message)
    elif instance.status == 'ACCEPTED':
        message = f'Problema ta "{instance.title}" a fost acceptată.'
        Notification.objects.create(user=instance.created_by, message=message)
