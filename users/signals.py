from django.db.models.signals import post_save
from django.dispatch import receiver

from subscribes.models import Recipients
from users.models import User


@receiver(post_save, sender=User, weak=False, dispatch_uid="user_post_save_handler")
def member_pre_save_handler(sender, instance: User, created, *args, **kwargs):
    if created:
        try:
            Recipients(email=instance.email, author=instance).save()
        except:
            pass
