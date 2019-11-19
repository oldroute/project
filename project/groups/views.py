from django.shortcuts import render, Http404
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from project.groups.models import Group, GroupCourse, GroupMember
from project.groups.forms import GroupSearchForm


class GroupListView(View):

    def get(self, request, *args, **kwargs):
        objects = Group.objects.filter(show=True)
        search = request.GET.get('search')
        form = GroupSearchForm(data=request.GET)
        if search:
            objects = objects.filter(title__icontains=search)

        return render(
            template_name='groups/groups_list.html',
            context={
                'objects': objects,
                'form': form
            },
            request=request
        )


class GroupView(View):

    def get_object(self,  *args, **kwargs):
        try:
            return Group.objects.get(id=kwargs['group_id'])
        except:
            raise Http404

    def get(self, request, *args, **kwargs):

        group = self.get_object(*args, **kwargs)

        return render(
            template_name='groups/group.html',
            context={
                'object': group,
            },
            request=request
        )


@method_decorator(login_required, name='dispatch')
class GroupCourseView(View):

    def get_object(self, *args, **kwargs):
        try:
            return GroupCourse.objects.select_related('group', 'course').get(id=kwargs['group_course_id'])
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        group_course = self.get_object(*args, **kwargs)
        group = group_course.group
        if(request.user == group.author or request.user in group.members.all()):
            return render(
                request=request,
                template_name='groups/group_course.html',
                context={
                    'object': group_course,
                    'course_data': group_course.course.get_cache_data()
                }
            )
        else:
            raise Http404


@method_decorator(login_required, name='dispatch')
class GroupCourseSolutionsView(View):

    def get_object(self, *args, **kwargs):
        try:
            return GroupCourse.objects.select_related('group', 'course').get(id=kwargs['group_course_id'])
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        group_course = self.get_object(request, *args, **kwargs)
        group = group_course.group
        course = group_course.course
        result = {}
        for user in group.members.all():
            result['member-%d' % user.id] = {
                'full_name': user.get_full_name(),
                'data': user.get_cache_course_solutions_data(course),
                'show_link': request.user == group.author or request.user == user
            }
        return JsonResponse(result)

# class GroupsView(generic.ListView):
#     template_name = 'groups/groups.html'
#     context_object_name = 'groups'
#     paginate_by = 20
#
#     def get_queryset(self):
#         search = self.request.GET.get('search')
#         if search:
#             return Group.objects.filter(Q(name__icontains=search))
#         return Group.objects.all()
#
#
# class MyGroupsView(generic.ListView):
#     template_name = 'groups/my_groups.html'
#     context_object_name = 'groups'
#     paginate_by = 20
#
#     def get_queryset(self):
#         search = self.request.GET.get('search')
#         my_groups = self.request.user.ownership.all()\
#             .union(self.request.user.membership.all())
#         if search:
#             return my_groups.filter(Q(name__icontains=search))
#         return my_groups
#
#
# class GroupView(generic.DetailView):
#     model = Group
#     template_name = 'groups/group.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(GroupView, self).get_context_data(**kwargs)
#         group = context['group']
#         context['members'] = group.members.all()
#         if self.request.user.is_authenticated:
#             context['is_member'] = self.request.user in group.get_members()
#         else:
#             context['is_member'] = False
#         context['position'] = group.get_user_position(self.request.user)
#         context['modules_data'] = group.group_module.all()
#         courses = []
#         for course_item in group.course_items.all():
#             courses.append({
#                 'title': course_item.course.title,
#                 'url': '/groups/%d/courses/%d/' % (group.id, course_item.course.id)
#             })
#         context['courses'] = courses
#
#         return context
#
#
# class GroupCourse(View):
#
#     template = 'groups/group_course.html'
#
#     def get(self, request, group_id, course_id):
#         group = get_object_or_404(Group, id=group_id)
#         if request.user in group.get_members():
#             course_item = get_object_or_404(group.course_items, course__id=course_id)
#             themes = course_item.course.get_descendants().filter(type=TreeItem.THEME, in_number_list=True, show=True)
#             context = {
#                 'course_data': course_item.get_course_data(themes.first()),
#                 'group': group,
#                 'course': course_item.course,
#                 'show_solutions_links': request.user.is_superuser,
#                 'themes_ids': list(themes.exclude(id=themes.first().id).values_list('id', flat=True))[::-1]
#             }
#             return render(request, self.template, context)
#         raise Http404
#
#
# def group_course_theme(request, group_id, course_id, theme_id):
#
#     group = get_object_or_404(Group, id=group_id)
#     if request.user in group.get_members():
#         course_item = get_object_or_404(group.course_items, course__id=course_id)
#         theme = TreeItem.objects.get(id=theme_id)
#     data = course_item.get_course_data(theme)
#     context = {
#         'table':  data['tables'][0],
#         'group': group,
#         'show_solutions_links': request.user.is_superuser,
#     }
#     table_html = render_to_string('groups/includes/group_course_table.html', context, request)
#     del data['members_col'][-1]
#     return JsonResponse({
#         'table': table_html,
#         'members_col': data['members_col']
#     })
#
#
# # TODO Переделать. 1. Создать и согласовать json-структуру таблицы. 2 GroupModule лишнее звено - сохранять в кэш
# class GroupProgressView(generic.DetailView):
#     model = Group
#     template_name = 'groups/progress.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(GroupProgressView, self).get_context_data(**kwargs)
#
#         get_object_or_404(context['group'].owners, pk=self.request.user.pk)
#
#         context['tables'] = []
#         members = context['group'].members.all()
#         for group_module in context['group'].group_module.all():
#             table_data = group_module.get_solutions_as_table(members)
#             context['tables'].append(table_data)
#
#         return context
#
#
# def join(request, group_id):
#     group = get_object_or_404(Group, pk=group_id)
#
#     if group.members.filter(pk=request.user.pk):
#         group.members.remove(request.user)
#         messages.info(request, 'Вы больше не участник группы "{}".'.format(group.name))
#         return HttpResponseRedirect(reverse('groups:my_groups'))
#     elif group.owners.filter(pk=request.user.pk):
#         if group.owners.all()[0].pk != request.user.pk:
#             group.owners.remove(request.user)
#             messages.info(request, 'Вы больше не владелец группы "{}".'.format(group.name))
#             return HttpResponseRedirect(reverse('groups:my_groups'))
#     elif group.state != group.CLOSE:
#         if group.state == group.CODE and request.POST['codeword'] != group.codeword:
#             messages.error(request, 'Неверное кодовое слово!')
#             return HttpResponseRedirect(reverse('groups:group', args=(group.pk, )))
#         group.members.add(request.user)
#         messages.info(request, 'Вы вступили в группу "{}".'.format(group.name))
#
#     return HttpResponseRedirect(reverse('groups:group', args=(group.pk, )))
