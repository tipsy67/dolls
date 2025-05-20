from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.models import BlogArticle



@receiver(post_save, sender=BlogArticle, weak=False, dispatch_uid="post_save_image")
def image_post_save(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(
            lambda: resize_image.delay(instance.pk))