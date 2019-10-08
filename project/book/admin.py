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

import copy
import json
import operator
from collections import OrderedDict
from functools import partial, reduce, update_wrapper

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.admin import helpers, widgets
from django.contrib.admin.checks import (
    BaseModelAdminChecks, InlineModelAdminChecks, ModelAdminChecks,
)
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import (
    NestedObjects, construct_change_message, flatten_fieldsets,
    get_deleted_objects, lookup_needs_distinct, model_format_dict, quote,
    unquote,
)
from django.contrib.auth import get_permission_codename
from django.core.exceptions import (
    FieldDoesNotExist, FieldError, PermissionDenied, ValidationError,
)
from django.core.paginator import Paginator
from django.db import models, router, transaction
from django.db.models.constants import LOOKUP_SEP
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms.formsets import DELETION_FIELD_NAME, all_valid
from django.forms.models import (
    BaseInlineFormSet, inlineformset_factory, modelform_defines_fields,
    modelform_factory, modelformset_factory,
)
from django.forms.widgets import CheckboxSelectMultiple, SelectMultiple
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseBase
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.urls import reverse
from django.utils import six
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import format_html
from django.utils.http import urlencode, urlquote
from django.utils.safestring import mark_safe
from django.utils.text import capfirst, format_lazy, get_text_list
from django.utils.translation import ugettext as _, ungettext
from django.views.decorators.csrf import csrf_protect
from django.views.generic import RedirectView

IS_POPUP_VAR = '_popup'
TO_FIELD_VAR = '_to_field'

HORIZONTAL, VERTICAL = 1, 2

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
    exclude = ('order_key',)
    list_display = ('title', 'course', 'author', 'show')
    inlines = (TaskItemInline,)

    def __init__(self, model, admin_site, course=None):
        super().__init__(model, admin_site)
        print('====init====', course)
        self._course = course

    def save_model(self, request, obj, form, change):
        obj.course = self._course
        obj.order_key = Topic.objects.filter(course=self._course).count()
        print('====save====', obj.course)
        obj.save()

    def add_topic(self, request, course_pk):

        course = self.get_object_with_change_permissions(request, Course, course_pk)
        course_admin = TopicAdmin(Topic, self.admin_site, course)
        return course_admin.add_view(request, extra_context={'course': course})

    def change_topic(self, request, course_pk):

        course = self.get_object_with_change_permissions(request, Course, course_pk)
        course_admin = TopicAdmin(Topic, self.admin_site, course)
        return course_admin.change_view(request, extra_context={'course': course})

    def get_urls(self):
        return [
            url(r'^(?P<course_pk>[0-9]+)/topics/add/$', self.admin_site.admin_view(self.add_topic), name='add_topic'),
            url(r'^(?P<course_pk>[0-9]+)/topics/change/$', self.admin_site.admin_view(self.change_topic), name='change_topic'),
        ] + super().get_urls()

    # def response_add(self, request, obj, post_url_continue=None):
    #     """
    #     Determines the HttpResponse for the add_view stage.
    #     """
    #
    #     opts = obj._meta
    #     pk_value = obj._get_pk_val()
    #     preserved_filters = self.get_preserved_filters(request)
    #     obj_url = reverse(
    #         'admin:%s_%s_change' % (opts.app_label, opts.model_name),
    #         args=(quote(pk_value),),
    #         current_app=self.admin_site.name,
    #     )
    #     # Add a link to the object's change form if the user can edit the obj.
    #     if self.has_change_permission(request, obj):
    #         obj_repr = format_html('<a href="{}">{}</a>', urlquote(obj_url), obj)
    #     else:
    #         obj_repr = force_text(obj)
    #     msg_dict = {
    #         'name': force_text(opts.verbose_name),
    #         'obj': obj_repr,
    #     }
    #     # Here, we distinguish between different save types by checking for
    #     # the presence of keys in request.POST.
    #
    #     if IS_POPUP_VAR in request.POST:
    #         to_field = request.POST.get(TO_FIELD_VAR)
    #         if to_field:
    #             attr = str(to_field)
    #         else:
    #             attr = obj._meta.pk.attname
    #         value = obj.serializable_value(attr)
    #         popup_response_data = json.dumps({
    #             'value': six.text_type(value),
    #             'obj': six.text_type(obj),
    #         })
    #         return TemplateResponse(request, self.popup_response_template or [
    #             'admin/%s/%s/popup_response.html' % (opts.app_label, opts.model_name),
    #             'admin/%s/popup_response.html' % opts.app_label,
    #             'admin/popup_response.html',
    #         ], {
    #             'popup_response_data': popup_response_data,
    #         })
    #
    #     # Redirecting after "Save as new".
    #     elif "_continue" in request.POST or ("_saveasnew" in request.POST and self.save_as_continue and self.has_change_permission(request, obj)):
    #         print('==1==')
    #         msg = format_html(_('The {name} "{obj}" was added successfully. You may edit it again below.'), **msg_dict)
    #         self.message_user(request, msg, messages.SUCCESS)
    #         if post_url_continue is None:
    #             post_url_continue = obj_url
    #         post_url_continue = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, post_url_continue)
    #         return HttpResponseRedirect(post_url_continue)
    #
    #     elif "_addanother" in request.POST:
    #         print('==2==')
    #         msg = format_html(_('The {name} "{obj}" was added successfully. You may add another {name} below.'), **msg_dict)
    #         self.message_user(request, msg, messages.SUCCESS)
    #         redirect_url = request.path
    #         redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
    #         print('===redirect_url===>', redirect_url)
    #         return HttpResponseRedirect(redirect_url)
    #
    #     else:
    #         print('==3==')
    #         msg = format_html(_('The {name} "{obj}" was added successfully.'), **msg_dict)
    #         self.message_user(request, msg, messages.SUCCESS)
    #         return self.response_post_save_add(request, obj)
    def response_change(self, request, obj):

        opts = self.model._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)

        msg_dict = {'name': force_text(opts.verbose_name), 'obj': format_html('<a href="{}">{}</a>', urlquote(request.path), obj),}
        if "_continue" in request.POST:
            msg = format_html(
                _('The {name} "{obj}" was changed successfully. You may edit it again below.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)

        elif "_saveasnew" in request.POST:
            msg = format_html(
                _('The {name} "{obj}" was added successfully. You may edit it again below.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = reverse('admin:%s_%s_change' % (opts.app_label, opts.model_name), args=(pk_value,), current_app=self.admin_site.name)
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)

        elif "_addanother" in request.POST:
            msg = format_html(_('The {name} "{obj}" was changed successfully. You may add another {name} below.'), **msg_dict)
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = reverse('admin:%s_%s_add' % (opts.app_label, opts.model_name), current_app=self.admin_site.name)
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)

        else:
            msg = format_html(_('The {name} "{obj}" was changed successfully.'), **msg_dict)
            self.message_user(request, msg, messages.SUCCESS)
            return self.response_post_save_change(request, obj)



@admin.register(Course)
class CourseAdmin(SortableAdminMixin, admin.ModelAdmin):

    model = Course
    list_display = ('order_key', 'title', 'author', 'show')
    list_display_links = ('title',)
    inlines = [TopicInline]
    exclude = ('order_key',)
    raw_id_fields = ("author",)

    def set_instance(self, request):
        object_id = int(request.META['PATH_INFO'].strip('/').split('/')[-2])
        self.instance = self.model.objects.get(pk=object_id)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.set_instance(request)
        return self.changeform_view(request, object_id, form_url, extra_context)

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
