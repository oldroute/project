# -*- coding:utf-8 -*-
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import HttpResponse, render, get_object_or_404, Http404
from django.core.exceptions import PermissionDenied
from django.views.generic import View
from .models import *


def courses(request):
    return HttpResponse('OK')


def course(request, slug):
    return HttpResponse('OK')


def course_total(request, slug, group_pk):
    return HttpResponse('OK')


def topic(request, slug, topic_pk):
    return HttpResponse('OK')


class TaskItemView(View):

    def get(self, request, **kwargs):
        taskitem = get_object_or_404(TaskItem, id=kwargs['taskitem_pk'])
        context = {'object': taskitem}

        return render(request, 'training/taskitem.html', context)


def solution(request, solution_id):
    return HttpResponse('OK')
