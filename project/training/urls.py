from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.courses, name='courses'),
    url('^(?P<slug>[a-z0-9-]+)/$', views.course, name='course'),
    url('^(?P<slug>[a-z0-9-]+)/total-(?P<group_pk>\d+)/$', views.course_total, name='course-total'),
    url('^(?P<slug>[a-z0-9-]+)/(?P<topic_pk>\d+)/$', views.TopicView.as_view(), name='topic'),
    url('^(?P<slug>[a-z0-9-]+)/(?P<topic_pk>\d+)/(?P<taskitem_pk>\d+)/$', views.TaskItemView.as_view(), name='taskitem'),
    url('^(?P<slug>[a-z0-9-]+)/(?P<topic_pk>\d+)/(?P<taskitem_pk>\d+)/solution/$', views.solution, name='solution'),
]
