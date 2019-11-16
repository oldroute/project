# -*- coding:utf-8 -*-
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, Http404
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from project.training.models import TaskItem, Solution, Course
from project.training.forms import TaskItemForm


UserModel = get_user_model()


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
            context={
                'course': taskitem.topic.course,
                'object': taskitem,
                'solution': solution,
                'form': form
            }
        )

    def post(self, request, *args, **kwargs):
        taskitem = self.get_object(request)
        form = TaskItemForm(data=request.POST)
        response = form.perform_operation(request.user, taskitem)
        return JsonResponse(response.__dict__)


class SolutionView(View):

    def get_object(self, request):
        if request.user.is_active:
            solution_user_id = request.GET.get('user')
            if solution_user_id:
                if request.user.is_superuser:
                    try:
                        return Solution.objects.get(url=request.path, user_id=solution_user_id)
                    except Solution.DoesNotExist:
                        raise Http404
                else:
                    raise PermissionDenied
            else:
                try:
                    return Solution.objects.get(url=request.path, user_id=request.user.id)
                except Solution.DoesNotExist:
                    raise Http404
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        solution = self.get_object(request)
        return render(
            request,
            template_name='training/solution.html',
            context={
                'object': solution,
                'course': solution.taskitem.topic.course
            }
        )


@method_decorator(login_required, name='dispatch')
class CourseSolutionsView(View):

    def get(self, request, *args, **kwargs):
        try:
            course = Course.objects.get(slug=kwargs.get('course'))
            user_id = request.GET['user_id']
            user = UserModel.objects.get(id=user_id, is_active=True)
            return JsonResponse(user.get_cache_course_solutions_data(course))
        except:
            raise Http404
