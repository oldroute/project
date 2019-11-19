from django.db import models
from django.contrib.auth import get_user_model
from project.training.models import Course
from tinymce.models import HTMLField


UserModel = get_user_model()


class Group(models.Model):

    class Meta:
        verbose_name = 'учебная группа'
        verbose_name_plural = 'учебные группы'

    OPEN = '0'
    CLOSE = '1'
    CODE = '2'
    CHOICES = (
        (OPEN, 'Открыта'),
        (CLOSE, 'Закрыта'),
        (CODE, 'Кодовое слово'),
    )

    show = models.BooleanField(verbose_name="отображать", default=True)
    title = models.CharField(verbose_name='название', max_length=255)
    author = models.ForeignKey(UserModel, verbose_name='автор')
    status = models.CharField(verbose_name='cтатус', choices=CHOICES, default=CLOSE, max_length=255)
    codeword = models.CharField(verbose_name='кодовое слово', blank=True, null=True, max_length=255)
    content = HTMLField(verbose_name='описание', blank=True, null=True)
    creation_date = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    members = models.ManyToManyField(UserModel, through='GroupMember', related_name='training_groups')

    def __str__(self):
        return self.title

    def get_status(self):
        for choice in self.CHOICES:
            if self.status == choice[0]:
                return choice[1]

    # def get_absolute_url(self):
    #     return reverse('groups')


class GroupMember(models.Model):

    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'участники'

    user = models.ForeignKey(UserModel, verbose_name='участник', related_name='member')
    group = models.ForeignKey(Group, related_name='member')

    def __str__(self):
        return self.user.get_full_name()


class GroupCourse(models.Model):

    class Meta:
        verbose_name = 'учебный курс'
        verbose_name_plural = 'учебные курсы'
        unique_together = ['group', 'course']

    group = models.ForeignKey(Group, related_name='group_courses')
    course = models.ForeignKey(Course, verbose_name='курс', limit_choices_to={'show': True})

    def __str__(self):
        return self.course.__str__()


#
# #####################
# class Group(models.Model):
#     OPEN = 0
#     CLOSE = 1
#     CODE = 2
#     STATES = (
#         (OPEN, 'Открыта'),
#         (CLOSE, 'Закрыта'),
#         (CODE, 'Кодовое слово'),
#     )
#
#     ROOT = 100
#     OWNER = 90
#     MEMBER = 50
#     NONE = 10
#
#     name = models.CharField(max_length=64, help_text='Введите название группы', verbose_name='Название')
#     status = models.TextField(max_length=1024, help_text='Введите статус группы', verbose_name='Статус', blank=True)
#     changed_status = models.DateTimeField(default=timezone.now)
#     owners = models.ManyToManyField(User, verbose_name='Владельцы', related_name='ownership')
#     members = models.ManyToManyField(User, verbose_name='Участники', related_name='membership', blank=True)
#     state = models.IntegerField(verbose_name='Статус', choices=STATES, default=CLOSE)
#     codeword = models.CharField(max_length=64, help_text='Введите кодовое слово', verbose_name='Код', blank=True)
#     created_at = models.DateTimeField(verbose_name='Создана', auto_now_add=True)
#
#     class Meta:
#         verbose_name = 'Учебная группа'
#         verbose_name_plural = 'Учебные группы'
#
#     def __str__(self):
#         return self.name
#
#     @classmethod
#     def from_db(cls, db, field_names, values):
#         instance = super(Group, cls).from_db(db, field_names, values)
#         instance.__status = values[field_names.index('status')]
#         return instance
#
#     def get_absolute_url(self):
#         return reverse('groups:group', args=(self.pk, ))
#
#     def get_state(self):
#         return self.STATES[self.state][1]
#
#     def get_root_username(self):
#         try:
#             return self.owners.all()[0].get_full_name()
#         except IndexError:
#             return 'None'
#
#     get_root_username.short_description = 'Владелец'
#
#     def get_owners_usernames(self):
#         return ' ,'.join([owner.get_full_name() or owner.username for owner in self.owners.all()])
#
#     def get_members(self):
#         return self.owners.all()\
#             .union(self.members.all())
#
#     def get_members_number(self):
#         return self.owners.count() + self.members.count()
#
#     get_members_number.short_description = 'Участников'
#
#     def get_user_position(self, user):
#         if user.is_authenticated():
#             if self.members.filter(pk=user.pk):
#                 return Group.MEMBER
#             elif self.owners.filter(pk=user.pk):
#                 if self.owners.all()[0].pk == user.pk:
#                     return Group.ROOT
#                 return Group.OWNER
#         return Group.NONE
#
#     def save(self, force_insert=False, force_update=False, using=None,
#              update_fields=None):
#         if not self._state.adding and self.__status != self.status:
#             self.changed_status = timezone.now
#         super(Group, self).save(force_insert, force_update, using, update_fields)
#
#
# class GroupCourse(models.Model):
#
#     group = models.ForeignKey(Group, related_name='course_items')
#     course = models.ForeignKey(TreeItem, verbose_name='курс', limit_choices_to={'show': True, 'type': TreeItem.COURSE})
#
#     def get_course_data(self, theme):
#         members = self.group.members.filter(is_active=True)
#         tables = []
#         members_col = OrderedDict({-1: {'name': 'Участник', 'score': 'Решено'}})
#         for member in members:
#             members_col[member.id] = {
#                 'name': member.last_name or member.username,
#                 'score': 0,
#                 'title': member.get_full_name()
#             }
#
#         tasks_ids = theme.get_descendants().filter(type=TreeItem.TASK, show=True).values_list("id", flat=True)
#         codes = Code.objects.filter(treeitem__in=tasks_ids, save_solutions=True).order_by("treeitem__lft")
#         thead = []
#         for code in codes:
#             th = {
#                 "text": code.get_order_number(),
#                 "url": code.treeitem.get_absolute_url(),
#                 "title": code.get_title()
#             }
#             thead.append(th)
#         tbody = []
#         for user in members:
#             tr = []
#             for code in codes:
#                 status, text, url = '', '', ''
#                 solution_time = ''
#                 user_solution = UserSolution.objects.filter(user=user, code=code).first()
#                 if user_solution:
#                     status = user_solution.status
#                     solution_time = user_solution.best_time
#                     if status == UserSolution.SUCCESS:
#                         text = '+'
#                         members_col[user.id]['score'] += 1
#                     elif status == UserSolution.PROCESS:
#                         text = str(user_solution.progress) + "%"
#                     elif status == UserSolution.UNLUCK:
#                         text = "-"
#                     url = reverse('user_solution', kwargs={"user_id": user.id, "code_id": code.id})
#
#                 title = '%s  %s\n%s' % (user.get_full_name(), solution_time, code.get_title())
#                 tr.append({
#                     "text": text,
#                     "url": url,
#                     "status": status,
#                     "title": title,
#                 })
#             tbody.append(tr)
#         tables.append({
#             'caption': theme.tree_name,
#             'thead': thead,
#             'tbody': tbody
#         })
#         return {
#             'tables': tables,
#             'members_col': members_col,
#         }