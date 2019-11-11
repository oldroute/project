from django.db import models


class OrderField(models.PositiveIntegerField):

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, instance, add):
        if getattr(instance, self.attname) is None:
            # Значение пусто
            qst = self.model.objects.all()
            try:
                if self.for_fields:
                    # Фильтруем обьекты с такими же значениями полей
                    # перечисленных в for_fields
                    query = {field: getattr(instance, field) for field in self.for_fields}
                    qst = qst.filter(**query)
                value = qst.latest(self.attname).order_key + 1
            except:
                value = 0
            setattr(instance, self.attname, value)
            return value
        else:
            return super().pre_save(instance, add)