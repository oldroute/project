from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from django.urls import reverse
from project.langs.models import Lang
from project.training.fields import OrderField


UserModel = get_user_model()


class Course(models.Model):
    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ['order_key']

    show = models.BooleanField(verbose_name="отображать", default=True)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    slug = models.SlugField(verbose_name="слаг", max_length=255, unique=True)
    lang = models.ForeignKey(Lang, verbose_name="язык программирования")
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)
    about = HTMLField(verbose_name="краткое описание", default="", blank=True, null=True)
    content = HTMLField(verbose_name="текстовый контент", default="", blank=True, null=True)
    content_bottom = HTMLField(verbose_name="текстовый контент под списком тем", default="", blank=True, null=True)

    order_key = OrderField(verbose_name='порядок', blank=True)
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)
    url = models.CharField(max_length=1000, blank=True, null=True)

    @property
    def topics(self):
        return self._topics.filter(show=True)

    def __str__(self):
        return self.title

    def get_breadcrumbs(self):
        return [
            {'title': 'Курсы', 'url': reverse('training:courses')},
        ]

    def update_cache_data(self):
        self.url = reverse('training:course', kwargs={'course': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_cache_data()
        super().save()
        for topic in self.topics:
            topic.save()

    def get_absolute_url(self):
        return self.url
