from django.apps import AppConfig


class ProfileAppConfig(AppConfig):

    name = 'project.profile'

    def ready(self):
        from django.contrib.auth import get_user_model

        UserModel = get_user_model()

        def cache_course_key(self, course):
            return 'user-%d-course-%d' % (self.id, course.id)

        def get_course_solutions_data(self, course):
            from project.training.models import Solution
            data = {}
            for solution in Solution.objects.select_related('taskitem').filter(user=self, taskitem__topic__course=course):
                data['taskitem__%d' % solution.taskitem.id] = solution.status
            return data

        def get_cache_course_solutions_data(self, course):
            import json
            from django.core.cache import cache
            json_data = cache.get(self.cache_course_key(course))
            if not json_data:
                data = self.get_course_solutions_data(course)
                cache.set(self.cache_course_key(course), json.dumps(data, ensure_ascii=False))
            else:
                data = json.loads(json_data)
            return data

        def update_cache_course_solutions_data(self, course, solution):
            import json
            from django.core.cache import cache
            data = self.get_cache_course_solutions_data(course)
            data['taskitem__%d' % solution.taskitem.id] = solution.status
            cache.set(self.cache_course_key(course), json.dumps(data, ensure_ascii=False))

        setattr(UserModel, 'cache_course_key', cache_course_key)
        setattr(UserModel, 'get_course_solutions_data', get_course_solutions_data)
        setattr(UserModel, 'get_cache_course_solutions_data', get_cache_course_solutions_data)
        setattr(UserModel, 'update_cache_course_solutions_data', update_cache_course_solutions_data)
