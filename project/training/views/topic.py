from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render, Http404
from project.training.forms import ContentForm
from project.training.models import Topic


class TopicView(View):

    def get_object(self, request, *args, **kwargs):
        try:
            return Topic.objects.select_related('course__lang').get(url=request.path)
        except Topic.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        topic = self.get_object(request)
        return render(
            request=request,
            template_name='training/topic/template.html',
            context={
                'object': topic,
                'course': topic.course,
            }
        )

    def post(self, request, *args, **kwargs):
        topic = self.get_object(request)
        form = ContentForm(data=request.POST)
        response = form.perform_operation(topic)
        return JsonResponse(response.__dict__)