# -*- coding:utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, Http404
from django.views.generic import View
from project.training.models import TaskItem, Solution
from project.training.forms import TaskItemForm


class TaskItemView(View):

    def get_object(self, request):
        try:
            return TaskItem.objects \
                .select_related('task', 'topic__course', 'topic__course__lang') \
                .get(url=request.path)
        except TaskItem.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        taskitem = self.get_object(request)
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

    def post(self, request, *args, **kwargs):
        taskitem = self.get_object(request)
        form = TaskItemForm(data=request.POST)
        response = form.perform_operation(request.user, taskitem)
        return JsonResponse(response.__dict__)


class SolutionView(View):

    def get_object(self, request):
        return

    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')
