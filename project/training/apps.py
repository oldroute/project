# -*- coding: utf-8 -*-
from django.apps import AppConfig


class TrainingAppConfig(AppConfig):

    name = "project.training"
    verbose_name = 'Учебные курсы'

    def ready(self):
        import project.training.signals
