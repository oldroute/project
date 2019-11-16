from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from project.training.models import Solution, TaskItem


@receiver(post_save, sender=Solution)
def solution_saved_handler(sender, instance, **kwargs):
    instance.user.update_cache_course_solutions_data(
        course=instance.taskitem.topic.course,
        solution=instance
    )


@receiver(post_save, sender=TaskItem)
@receiver(post_delete, sender=TaskItem)
def taskitem_changed_handler(sender, instance, **kwargs):
    cache.clear()
