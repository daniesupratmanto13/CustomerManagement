from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomerModel


@receiver(post_save, sender=User)
def customerProfile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        CustomerModel.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email
        )
