from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from project.training.models import Topic


@receiver(post_save, sender=Topic)
@receiver(post_delete, sender=Topic)
def topic_changed_handler(sender, instance, **kwargs):
    # TODO order_key пересчитывать
    cache.clear()
