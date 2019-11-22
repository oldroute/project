# -*- coding: utf-8 -*-
import re
from django.forms.models import model_to_dict
from django.db.models import Case, When
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from project.courses.models import TreeItem
from project.executors.models import Code, CodeTest, UserSolution
from project.sources.models import Source
from project.tasks.models import Source as TasksSourse
from project.langs.models import Lang
from project.tasks.models import Task

from project.training.models import Course, Topic, Content, TaskItem, Solution

UserModel = get_user_model()


class Command(BaseCommand):

    """ Сохранить записи курса для обновления порядкового номера """

    def handle(self, *args, **options):
        for topic in Topic.objects.filter(course_id=1):
            topic.save()
            for ts in topic.taskitems:
                ts.save()