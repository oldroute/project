from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^courses/', include('project.training.urls', namespace='training')),
    url(r'^courses/', include('project.courses.urls')),
    url(r'^executor/', include('project.executors.urls')),
    url(r'^groups/', include('project.groups.urls', namespace='groups')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^training/', include('project.training.urls')),
    url(r'^$', TemplateView.as_view(template_name='frontpage.html'))
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
#

