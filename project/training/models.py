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

    show = models.BooleanField(verbose_name="отображать", default=False)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    slug = models.SlugField(verbose_name="слаг", max_length=255, unique=True)
    lang = models.ForeignKey(Lang, verbose_name="язык программирования")
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)
    content = HTMLField(verbose_name="содержимое", default="", blank=True, null=True)

    order_key = models.PositiveIntegerField(verbose_name='порядок', default=1)
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)
    url = models.CharField(max_length=1000, blank=True, null=True)

    @property
    def topics(self):
        return self._topics.filter(show=True)

    def __str__(self):
        return self.title

    def update_cache_data(self):
        self.url = reverse('training:course', kwargs={'slug': self.slug})
        self.save()
        for topic in self.topics:
            topic.update_cache_data()

    def get_absolute_url(self):
        return self.url


class Topic(models.Model):
    class Meta:
        verbose_name = "тема"
        verbose_name_plural = "темы"
        ordering = ('order_key',)

    show = models.BooleanField(verbose_name="отображать", default=False)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)
    content = HTMLField(verbose_name="содержимое", default="", blank=True, null=True)

    course = models.ForeignKey(Course, verbose_name='курс', related_name='_topics')
    order_key = models.PositiveIntegerField(verbose_name='порядок', default=1)
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

    def update_cache_data(self):
        self.url = reverse(
            'training:topic', kwargs={'slug': self.course.slug, 'topic_pk': self.id}
        )
        self.save()
        for taskitem in self.taskitems:
            taskitem.update_cache_data()

    def get_absolute_url(self):
        return self.url


class TaskItem(models.Model):

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
        ordering = ('order_key',)

    show = models.BooleanField(verbose_name="отображать", default=False)
    task = models.ForeignKey(Task, verbose_name='задача', related_name='topics')

    order_key = models.PositiveIntegerField(verbose_name='порядок', default=0)
    number = models.CharField(max_length=255, blank=True, null=True)
    topic = models.ForeignKey(Topic, verbose_name='тема', related_name='_taskitems')
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)

    @property
    def lang(self):
        return self.topic.lang

    def __str__(self):
        return self.title

    def update_cache_data(self):
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
        self.save()

    def get_absolute_url(self):
        return self.url


class TaskSolution(models.Model):

    class Meta:
        verbose_name = "решение задачи"
        verbose_name_plural = "решения задач"

    # Статус решения
    SUCCESS = 'success'
    PROCESS = 'process'
    UNLUCK  = 'unluck'
    NONE    = 'none'

    taskitem = models.ForeignKey(TaskItem, verbose_name='задача')
    user = models.ForeignKey(UserModel, verbose_name="пользователь")
    last_changes = JSONField(verbose_name="последние изменения", blank=True, null=True)
    best = JSONField(verbose_name="лучшее решение", blank=True, null=True)
    versions = JSONField(verbose_name="сохраненные решения", default=list)
    url = models.CharField(max_length=1000, blank=True, null=True)

    def get_formated_time(self, str_date):

        d = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S.%f')
        return d.strftime('%Y.%m.%d [%H:%M]')

    @property
    def best_time(self):
        if self.best:
            return self.get_formated_time(self.best['datetime'])
        else:
            return ''

    @property
    def progress(self):
        if self.best is None:
            return None
        else:
            return int(self.best['progress'])

    @property
    def status_success(self):
        return self.progress == 100

    @property
    def status_process(self):
        return self.progress != 100

    @property
    def status_unluck(self):
        return self.progress == 0

    @property
    def status_none(self):
        return self.best is None

    @property
    def status(self):
        if self.status_none:
            return self.NONE
        else:
            if self.status_success:
                return self.SUCCESS
            elif self.status_unluck:
                return self.UNLUCK
            else:
                return self.PROCESS

    def __create_version(self, data):

        return {
            "datetime": data['datetime'],
            "input": data.get('input', ''),
            "content": data['content'],
            "progress": data['progress'],
            "tests": {
                'num': data.get("num", ''),
                'num_success': data.get("success_num", ''),
            }
        }

    def update_best(self, data=None, version=None):
        if not version:
            version = self.__create_version(data)

        self.last_changes = version
        if self.best is None:
            self.best = version
        else:
            if int(version['progress']) > self.progress:
                self.best = version

    def add_version(self, data):
        version = self.__create_version(data)
        self.last_changes = version
        self.versions.append(json.dumps(version, ensure_ascii=False))
        self.update_best(version=version)

    def get_versions(self):
        data = []
        for json_version in self.versions:
            version = json.loads(json_version)
            version['datetime'] = self.get_formated_time(version['datetime'])
            version['content'] = {
                'name': 'content',
                'value': version['content'],
            }
            data.append(version)
        return data

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
        return self.id

    def get_absolute_url(self):
        return self.url


__all__ = ['Course', 'Topic', 'TaskItem', 'TaskSolution']
