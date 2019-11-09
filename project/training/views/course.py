from django.shortcuts import render, Http404, HttpResponse
from django.views.generic import View
from project.training.models import Course


class CourseListView(View):

    def get(self, request, *args, **kwargs):

        context = {
            'objects': Course.objects.filter(show=True)
        }
        return render(
            template_name='training/course_list.html',
            context=context,
            request=request
        )


class CourseView(View):

    def get_object(self, request):
        try:
            return Course.objects\
                .select_related('lang')\
                .get(url=request.path)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):

        context = {
            'object': self.get_object(request)
        }
        return render(
            template_name='training/course.html',
            context=context,
            request=request
        )

