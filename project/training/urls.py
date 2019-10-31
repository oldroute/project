from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.courses, name='courses'),
    url('^(?P<course>[a-z0-9-]+)/$', views.course, name='course'),
    url('^(?P<course>[a-z0-9-]+)/(?P<topic>[a-z0-9-]+)/$', views.TopicView.as_view(), name='topic'),
    url('^(?P<course>[a-z0-9-]+)/(?P<topic>[a-z0-9-]+)/(?P<taskitem>[a-z0-9-]+)/$', views.TaskItemView.as_view(), name='taskitem'),
    url('^(?P<course>[a-z0-9-]+)/(?P<topic>[a-z0-9-]+)/(?P<taskitem>[a-z0-9-]+)/solution/$', views.SolutionView.as_view(), name='solution'),
]
