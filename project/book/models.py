from django.db import models
from django.contrib.postgres.fields import JSONField
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from project.executors.models import Lang


UserModel = get_user_model()


class Base(models.Model):

    class Meta:
        abstract = True

    order_key = models.PositiveIntegerField(verbose_name='порядок', default=0)
    show = models.BooleanField(verbose_name="отображать", default=False)
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    slug = models.SlugField(verbose_name="слаг", max_length=255, unique=True)
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)
    content = HTMLField(verbose_name="содержимое", default="", blank=True, null=True)

    def __str__(self):
        return self.title


class Source(Base):

    class Meta:
        verbose_name = "источник материалов"
        verbose_name_plural = "источники материалов"
        ordering = ('order_key',)


class Course(Base):
    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ('order_key',)

    lang = models.ForeignKey(Lang, verbose_name="язык программирования")


class Topic(Base):
    class Meta:
        verbose_name = "тема"
        verbose_name_plural = "темы"
        ordering = ('order_key',)

    course = models.ForeignKey(
        Course, verbose_name='курс',
        related_name='topics',
        blank=True, null=True
    )


class Task(Base):

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
        ordering = ('order_key',)

    source = models.ForeignKey(Source, verbose_name="источник", on_delete=models.SET_NULL, null=True, blank=True)
    source_raw_id = models.CharField(verbose_name="id в источнике", max_length=255, null=True, blank=True)

    input_max = models.PositiveIntegerField(verbose_name="макс. символов в блоке ввода", default=100)
    content_max = models.PositiveIntegerField(verbose_name="макс. символов в блоке кода", default=1000)
    timeout = models.PositiveIntegerField(verbose_name="макс. время отладки одного теста", default=10, help_text='секунд')

    tests = JSONField(verbose_name='тесты', default=list, blank=True, null=True)

    @property
    def lang(self):
        return self.topic.course.lang


class TaskItem(models.Model):

    class Meta:
        ordering = ('order_key',)

    order_key = models.PositiveIntegerField(verbose_name='порядок', default=0)
    task = models.ForeignKey(Task, verbose_name='задача', related_name='topics')
    topic = models.ForeignKey(Topic, verbose_name='тема', related_name='tasks')

    def __str__(self):
        return ''
