# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from project.training.models import Topic

UserModel = get_user_model()


class Command(BaseCommand):

    """ Сохранить записи курса для обновления порядкового номера """

    def handle(self, *args, **options):
        for topic in Topic.objects.filter(course_id=1):
            topic.save()
            for ts in topic.taskitems:
                ts.save()