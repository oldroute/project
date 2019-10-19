from django import forms


class SolutionForm(forms.Form):

    def __init__(self, instance, **kwargs):
        kwargs['initial'] = {'last_changes': instance.last_changes}
        kwargs['prefix'] = kwargs.get('prefix', '0')
        self.id = '#%s-editor-form' % kwargs['prefix']
        super().__init__(**kwargs)

    input = forms.CharField(
        label="Ввод", required=False
    )

    content = forms.CharField(
        label="", required=False,
    )

    output = forms.CharField(
        label="Вывод", required=False,
    )
    error = forms.CharField(
        label="Ошибка", required=False,
    )


__all__ = ['SolutionForm']
