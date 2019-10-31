from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from project.training.models import TaskItem, Solution


class TaskItemInline(SortableInlineAdminMixin, admin.TabularInline):

    model = TaskItem
    extra = 0
    fields = ('order_key', 'task', 'show')
    raw_id_fields = ("task",)


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    model = Solution
    raw_id_fields = ('user',)
