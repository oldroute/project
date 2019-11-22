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

    """ Продублировать курс питона в C++"""

    def handle(self, *args, **options):
        cpp_course = Course.objects.get(id=2)
        for topic in Topic.objects.filter(course_id=1):
            fields = model_to_dict(topic, exclude=['id', 'course', 'last_modified', 'author'])
            fields['course'] = cpp_course
            fields['author'] = topic.author
            copy_topic = Topic.objects.create(**fields)
            for ts in topic.taskitems:
                ts_fields = model_to_dict(ts, exclude=['id', 'topic', 'task'])
                ts_fields['topic'] = copy_topic
                ts_fields['task'] = ts.task
                TaskItem.objects.create (**ts_fields)
            for content in topic._content.all():
                c_fields = model_to_dict(content, exclude=['id', 'topic'])
                c_fields['topic'] = copy_topic
                Content.objects.create(**c_fields)

