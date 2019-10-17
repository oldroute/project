# -*- coding: utf-8 -*-
from django.apps import AppConfig


class TrainingAppConfig(AppConfig):
    name = "project.training"

    def ready(self):
        from . import signals