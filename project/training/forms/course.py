from django import forms
from django.core.exceptions import ValidationError
from project.training.models import Topic


class TopicAdminForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = '__all__'

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Topic.objects.filter(course=self.instance.course, slug=slug).exclude(id=self.instance.id).exists():
            raise ValidationError('Значение не уникально в рамках курса')
        return self.cleaned_data['slug']