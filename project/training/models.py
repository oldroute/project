import json
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from datetime import datetime
from django.urls import reverse

from project.langs.models import Lang
from project.tasks.models import Task

UserModel = get_user_model()


class Course(models.Model):
    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ('order_key',)

    show = models.BooleanField(verbose_name="отображать", default=True)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    slug = models.SlugField(verbose_name="слаг", max_length=255, unique=True)
    lang = models.ForeignKey(Lang, verbose_name="язык программирования")
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)
    content = HTMLField(verbose_name="содержимое", default="", blank=True, null=True)

    order_key = models.PositiveIntegerField(verbose_name='порядок', blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)
    url = models.CharField(max_length=1000, blank=True, null=True)

    @property
    def topics(self):
        return self._topics.filter(show=True)

    def __str__(self):
        return self.title

    def update_cache_data(self):
        if self.order_key is None:
            self.order_key = Course.objects.all().count() + 1
        self.url = reverse('training:course', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_cache_data()
        super().save()
        for topic in self.topics:
            topic.save()

    def get_absolute_url(self):
        return self.url


class Topic(models.Model):
    class Meta:
        verbose_name = "тема"
        verbose_name_plural = "темы"
        ordering = ('order_key',)

    show = models.BooleanField(verbose_name="отображать", default=True)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)
    content = HTMLField(verbose_name="содержимое", default="", blank=True, null=True)

    course = models.ForeignKey(Course, verbose_name='курс', related_name='_topics')
    order_key = models.PositiveIntegerField(verbose_name='порядок', blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)
    url = models.CharField(max_length=1000, blank=True, null=True)

    @property
    def lang(self):
        return self.course.lang

    @property
    def taskitems(self):
        return self._taskitems.filter(show=True)

    @property
    def number(self):
        return self.order_key

    def __str__(self):
        return self.title

    @property
    def numbered_title(self):
        return '%s %s' % (self.number, self.title)

    def update_cache_data(self):
        if self.order_key is None:
            self.order_key = Topic.objects.filter(course=self.course).count()

        self.url = reverse(
            'training:topic', kwargs={'slug': self.course.slug, 'topic_pk': self.id}
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_cache_data()
        super().save()
        for taskitem in self.taskitems:
            taskitem.update_cache_data()

    def get_absolute_url(self):
        return self.url


class TaskItem(models.Model):

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
        ordering = ('order_key',)

    show = models.BooleanField(verbose_name="отображать", default=True)
    task = models.ForeignKey(Task, verbose_name='задача', related_name='topics')

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

    def __str__(self):
        return self.title

    def update_cache_data(self):
        if self.order_key is None:
            self.order_key = TaskItem.objects.all().count()
        self.number = '%s.%s' % (self.topic.order_key, self.order_key)
        self.title = self.task.title
        self.url = reverse(
            'training:taskitem',
            kwargs={
                'slug': self.topic.course.slug,
                'topic_pk': self.topic.id,
                'taskitem_pk': self.id
            }
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_cache_data()
        super().save()

    def get_absolute_url(self):
        return self.url


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
                'slug': self.taskitem.topic.course.slug,
                'topic_pk': self.taskitem.topic.id,
                'taskitem_pk': self.id
            }
        )
        self.save()

    def __str__(self):
        return '%s: %s' % (self.user.get_full_name(), self.taskitem.title)

    def get_absolute_url(self):
        return self.url


__all__ = ['Course', 'Topic', 'TaskItem', 'Solution']
