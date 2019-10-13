from django.db import models


class Lang(models.Model):

    class Meta:
        verbose_name = "язык программирования"
        verbose_name_plural = "языки программирования"

    title = models.CharField(verbose_name="заголовок", max_length=255)

    def __str__(self):
        return self.title
