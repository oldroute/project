from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Task, Source


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    model = Task
    exclude = ('order_key',)
    raw_id_fields = ("author",)


@admin.register(Source)
class SourceAdmin(SortableAdminMixin, admin.ModelAdmin):

    model = Source
