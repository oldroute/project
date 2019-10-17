from django.db.models.signals import post_save
from .models import *


def post_save_handler(sender, instance, created, **kwargs):
    post_save.disconnect(post_save_handler, Course)
    post_save.disconnect(post_save_handler, Topic)
    post_save.disconnect(post_save_handler, TaskItem)
    post_save.disconnect(post_save_handler, TaskSolution)

    instance.update_cache_data()

    post_save.connect(post_save_handler, Course)
    post_save.connect(post_save_handler, Topic)
    post_save.connect(post_save_handler, TaskItem)
    post_save.connect(post_save_handler, TaskSolution)

post_save.connect(post_save_handler, Course)
post_save.connect(post_save_handler, Topic)
post_save.connect(post_save_handler, TaskItem)
post_save.connect(post_save_handler, TaskSolution)
