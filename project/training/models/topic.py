from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from django.urls import reverse
from project.training.models import Course
from project.training.fields import OrderField


UserModel = get_user_model()


class Topic(models.Model):
    class Meta:
        verbose_name = "тема"
        verbose_name_plural = "темы"
        ordering = ['order_key']

    show = models.BooleanField(verbose_name="отображать", default=True)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    slug = models.SlugField(verbose_name="слаг", max_length=255)
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)

    course = models.ForeignKey(Course, verbose_name='курс', related_name='_topics')
    order_key = OrderField(verbose_name='порядок', blank=True, for_fields=['course'])
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

    @property
    def numbered_title(self):
        return '%s %s' % (self.number, self.title)

    def get_breadcrumbs(self):
        return [
            {'title': 'Курсы', 'url': reverse('training:courses')},
            {'title': self.course.title, 'url': self.course.url},
        ]

    def get_data(self):
        return {
            'title': self.title,
            'url': self.url,
            'children': [taskitem.get_data() for taskitem in self.taskitems]
        }

    def update_cache_data(self):
        self.url = reverse(
            'training:topic',
            kwargs={'course': self.course.slug, 'topic': self.slug}
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_cache_data()
        super().save()
        for taskitem in self.taskitems:
            taskitem.update_cache_data()

    def get_absolute_url(self):
        return self.url

    def __str__(self):
        return self.title


class Content(models.Model):

    class Meta:
        verbose_name = "блок контента"
        verbose_name_plural = "блоки контента"
        ordering = ['order_key']

    ACE  = 'ace'
    TEXT = 'text'
    CHOICES = (
        (ACE, 'код'),
        (TEXT, 'текст'),
    )

    input = models.TextField(verbose_name='Ввод', blank=True, null=True)
    content = models.TextField(verbose_name='Редактор', blank=True, null=True)
    show_input = models.BooleanField(verbose_name='Отображать ввод', default=False)
    show_debug = models.BooleanField(verbose_name='Отображать отладчик', default=True)
    readonly = models.BooleanField(verbose_name='Только для чтения', default=False)
    text = HTMLField(blank=True, null=True)
    type = models.CharField(verbose_name='тип', max_length=255, choices=CHOICES, default='text')
    topic = models.ForeignKey(Topic, related_name='_content')
    order_key = OrderField(verbose_name='порядок', blank=True, for_fields=['topic'])

    @property
    def lang(self):
        return self.topic.course.lang


__all__ = ['Course', 'Topic', 'Content']
