from django.shortcuts import HttpResponse
from django.views.generic import View
from project.training.models import Course, Topic


def courses(request, **kwargs):
    return HttpResponse('OK')


def course(request, **kwargs):
    return HttpResponse('OK')


