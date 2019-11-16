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
            json_data = cache.get(self.cache_course_key)
            if not json_data:
                data = self.get_course_solutions_data(course)
                cache.set(self.cache_course_key, json.dumps(data, ensure_ascii=False))
            else:
                data = json.loads(json_data)
            return data

        setattr(UserModel, 'cache_course_key', cache_course_key)
        setattr(UserModel, 'get_course_solutions_data', get_course_solutions_data)
        setattr(UserModel, 'get_cache_course_solutions_data', get_cache_course_solutions_data)
