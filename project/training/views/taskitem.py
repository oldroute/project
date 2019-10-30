# -*- coding:utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, Http404
from django.views.generic import View
from ..models import *
from ..forms import *


class TaskItemView(View):

    def get_object(self, **kwargs):
        try:
            return TaskItem.objects \
                .select_related('task', 'topic', 'topic__course', 'topic__course__lang') \
                .get(id=kwargs['taskitem_pk'], topic_id=kwargs['topic_pk'])
        except TaskItem.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        taskitem = self.get_object(**kwargs)
        solution = None
        form_initial = {'lang': taskitem.lang.provider}
        if request.user.is_active:
            solution = Solution.objects.filter(taskitem=taskitem, user=request.user).first()
            if solution:
                form_initial['content'] = solution.last_changes
        form = TaskItemForm(initial=form_initial)
        return render(
            request=request,
            template_name='training/taskitem/template.html',
            context={'object': taskitem, 'solution': solution, 'form': form}
        )

    def post(self, request, **kwargs):
        taskitem = self.get_object(**kwargs)
        form = TaskItemForm(data=request.POST)
        response = form.perform_operation(request.user, taskitem)
        return JsonResponse(response.__dict__)


def solution(request, **kwargs):
    return HttpResponse('OK')
