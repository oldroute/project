from django.contrib import admin
from django.views.generic import RedirectView
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from .models import Course, Topic, Task, TaskItem, Source
from functools import update_wrapper
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.utils.html import escape
from django.shortcuts import get_object_or_404
from django.conf.urls import url


class TopicInline(SortableInlineAdminMixin, admin.TabularInline):

    model = Topic
    extra = 0
    fields = ('order_key', 'title')
    show_change_link = True
    readonly_fields = ('title',)

    @property
    def template(self):
        return 'admin/adminsortable2/tabular.html'


class TaskItemInline(SortableInlineAdminMixin, admin.TabularInline):

    model = TaskItem
    extra = 0
    fields = ('order_key', 'task')
    raw_id_fields = ("task",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):

    raw_id_fields = ("author",)
    exclude = ('order_key', 'course')
    list_display = ('title', 'course', 'author', 'show')
    inlines = (TaskItemInline,)

    def __init__(self, model, admin_site, course=None):
        super().__init__(model, admin_site)
        self._course = course

    def save_model(self, request, obj, form, change):
        obj.course = self._course
        obj.order_key = Topic.objects.filter(course=self._course).count()
        obj.save()


@admin.register(Course)
class CourseAdmin(SortableAdminMixin, admin.ModelAdmin):

    model = Course
    list_display = ('order_key', 'title', 'author', 'show')
    list_display_links = ('title',)
    inlines = [TopicInline]
    exclude = ('order_key',)
    raw_id_fields = ("author",)

    def get_object_with_change_permissions(self, request, model, obj_pk):
        obj = get_object_or_404(model, pk=obj_pk)
        if not self.has_change_permission(request, obj):
            raise PermissionDenied
        return obj

    def add_topic(self, request, course_pk):

        course = self.get_object_with_change_permissions(request, Course, course_pk)
        course_admin = TopicAdmin(Topic, self.admin_site, course)
        return course_admin.add_view(request, extra_context={'course': course})

    def get_urls(self):
        return [
            url(r'^(?P<course_pk>[0-9]+)/topics/add/$', self.admin_site.admin_view(self.add_topic), name='add_topic'),
        ] + super().get_urls()


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    model = Task
    exclude = ('order_key',)
    raw_id_fields = ("author",)


@admin.register(Source)
class SourceAdmin(SortableAdminMixin, admin.ModelAdmin):

    model = Source
    list_display = ('order_key', 'title', 'author', 'show')
    exclude = ('order_key',)
    raw_id_fields = ("author",)
