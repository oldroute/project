from django.db.models.signals import post_save
from django.dispatch import receiver
from project.training.models import Solution


@receiver(post_save, sender=Solution)
def solution_saved_handler(sender, instance, **kwargs):
    instance.user.update_cache_course_solutions_data(
        course=instance.taskitem.topic.course,
        solution=instance
    )
