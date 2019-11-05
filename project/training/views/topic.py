from django.views.generic import View
from project.training.models import Topic
from django.shortcuts import render, Http404


class TopicView(View):

    def get_object(self, request):
        try:
            return Topic.objects.select_related('course__lang').get(url=request.path)
        except Topic.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        topic = self.get_object(request)
        return render(
            request=request,
            template_name='training/topic/template.html',
            context={'object': topic}
        )
