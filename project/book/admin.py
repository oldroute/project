from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from .models import Course, Topic, Task, TaskItem, Source


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


@admin.register(Course)
class CourseAdmin(SortableAdminMixin, admin.ModelAdmin):

    model = Course
    list_display = ('order_key', 'title', 'author', 'show')
    list_display_links = ('title',)
    inlines = [TopicInline]
    exclude = ('order_key',)
    raw_id_fields = ("author",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):

    raw_id_fields = ("author",)
    exclude = ('order_key',)
    list_display = ('title', 'course', 'author', 'show')
    inlines = (TaskItemInline,)


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
