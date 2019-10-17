from django.conf.urls import url
from . import views

app_name = 'training'
urlpatterns = [
    url('^$', views.courses, name='courses'),
    url('^(?P<slug>\w+)/', views.course, name='course'),
    url('^(?P<slug>\w+)/total-(?P<group_pk>\d+)/$', views.course_total, name='course-total'),
    url('^(?P<slug>\w+)/(?P<topic_pk>\d+)/$', views.topic, name='topic'),
    url('^(?P<slug>\w+)/(?P<topic_pk>\d+)/(?P<taskitem_pk>\d+)/', views.TaskItemView.as_view(), name='taskitem'),
    url('^(?P<slug>\w+)/(?P<topic_pk>\d+)/(?P<taskitem_pk>\d+)/solution/$', views.solution, name='solution'),
]
