from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from django.urls import reverse
from project.langs.models import Lang

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
        self.url = reverse('training:course', kwargs={'course': self.slug})

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
    slug = models.SlugField(verbose_name="слаг", max_length=255)
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)

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


class Content(models.Model):

    class Meta:
        verbose_name = "блок контента"
        verbose_name_plural = "блоки контента"
        ordering = ('order_key',)

    CHOICES = (
        ('ace', 'код'),
        ('text', ' текст'),
    )

    ace = models.TextField(blank=True, null=True)
    text = HTMLField(blank=True, null=True)
    type = models.CharField(verbose_name='тип', max_length=255, choices=CHOICES, default='text')
    topic = models.ForeignKey(Topic, related_name='content')
    order_key = models.PositiveIntegerField(verbose_name='порядок', blank=True, null=True)


__all__ = ['Course', 'Topic', 'Content']
