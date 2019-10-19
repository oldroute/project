# -*- coding:utf-8 -*-
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import HttpResponse, render, get_object_or_404, Http404
from django.core.exceptions import PermissionDenied
from django.views.generic import View
from ..models import *
from ..forms import *


class TaskItemView(View):

    def get(self, request, **kwargs):
        taskitem = TaskItem.objects.filter(id=kwargs['taskitem_pk']).select_related('task', 'topic', 'topic__course').first()
        solution = Solution.objects.filter(taskitem=taskitem, user=request.user).first()
        form = SolutionForm(instance=solution)
        context = {
            'object': taskitem,
            'solution': solution,
            'form': form
        }
        return render(request, 'training/taskitem/template.html', context)

    def post(self, request, **kwargs):
        print('===', kwargs)
        return HttpResponse('OK')


def solution(request):
    return HttpResponse('OK')
