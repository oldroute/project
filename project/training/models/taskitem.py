import random
from unidecode import unidecode
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from datetime import datetime
from django.urls import reverse
from django.utils.text import slugify
from project.tasks.models import Task
from project.training.models import Topic

UserModel = get_user_model()


class TaskItem(models.Model):

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
        ordering = ('order_key',)

    show = models.BooleanField(verbose_name="отображать", default=True)
    task = models.ForeignKey(Task, verbose_name='задача', related_name='topics')
    slug = models.SlugField(verbose_name="слаг", max_length=255, blank=True, null=True)

    order_key = models.PositiveIntegerField(verbose_name='порядок', blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    topic = models.ForeignKey(Topic, verbose_name='тема', related_name='_taskitems')
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)

    @property
    def lang(self):
        return self.topic.lang

    @property
    def solution_url(self):
        return self.url + 'solution/'

    @property
    def numbered_title(self):
        return '%s %s' % (self.number, self.title)

    def _set_slug(self):
        slug = slugify(unidecode(self.task.title))
        if TaskItem.objects.filter(topic=self.topic, slug=slug).exclude(id=self.id).exists():
             slug += str(random.randint(0, 999))
        self.slug = slug

    def update_cache_data(self):
        if self.order_key is None:
            self.order_key = TaskItem.objects.all().count()
        if self.slug is None:
            self._set_slug()

        self.number = '%s.%s' % (self.topic.order_key, self.order_key)
        self.title = self.task.title
        self.url = reverse(
            'training:taskitem',
            kwargs={
                'course': self.topic.course.slug,
                'topic': self.topic.slug,
                'taskitem': self.slug
            }
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_cache_data()
        super().save()

    def get_absolute_url(self):
        return self.url

    def __str__(self):
        return self.title


class Solution(models.Model):

    class Meta:
        verbose_name = "решение задачи"
        verbose_name_plural = "решения задач"

    class Status:
        NONE = '0'
        UNLUCK = '1'
        PROCESS = '2'
        SUCCESS = '3'
        CHOICES = (
            (NONE, 'нет попыток'),
            (UNLUCK, 'нет прогресса'),
            (PROCESS, 'есть прогресс'),
            (SUCCESS, 'решено'),
        )

    taskitem = models.ForeignKey(TaskItem, verbose_name='задача', related_name='_solution')
    user = models.ForeignKey(UserModel, verbose_name="пользователь")
    url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(verbose_name='статус', max_length=255,  choices=Status.CHOICES, default=Status.NONE)
    progress = models.PositiveIntegerField(verbose_name='Прогресс решения', blank=True, default=0)
    last_changes = models.CharField(verbose_name="последние изменения", max_length=255, blank=True, default='')
    version_best = JSONField(verbose_name="лучшее решение", blank=True, null=True)
    version_list = JSONField(verbose_name="список сохраненных решений", default=list, blank=True, null=True)

    def _create_version_data(self, content, tests_result):
        if tests_result['num_success'] > 0 and tests_result['num'] > 0:
            progress = round(100 * tests_result['num_success'] / tests_result['num'])
        else:
            progress = 0
        return {
            "datetime": str(datetime.now()),
            "content": content,
            "progress": progress,
            "tests": {
                'num': tests_result['num'],
                'num_success': tests_result['num_success'],
            }
        }

    def _set_status(self):
        if self.progress == 0:
            self.status = self.Status.UNLUCK
        elif self.progress == 100:
            self.status = self.Status.SUCCESS
        else:
            self.status = self.Status.PROCESS

    def update(self, content, tests_result):
        version = self._create_version_data(content, tests_result)
        self.last_changes = content
        if version['progress'] > self.progress:
            self.version_best = version
            self.progress = version['progress']
            self._set_status()

    def create_version(self, content, tests_result):
        version = self._create_version_data(content, tests_result)
        self.last_changes = content
        if version['progress'] > self.progress:
            self.version_best = version
            self.progress = version['progress']
            self._set_status()
        self.version_list.append(version)

    def update_cache_data(self):
        self.url = reverse(
            'training:solution',
            kwargs={
                'course': self.taskitem.topic.course.slug,
                'topic': self.taskitem.topic.slug,
                'taskitem': self.taskitem.slug
            }
        )
        self.save()

    def __str__(self):
        return '%s: %s' % (self.user.get_full_name(), self.taskitem.title)

    def get_absolute_url(self):
        return self.url


__all__ = ['TaskItem', 'Solution']
