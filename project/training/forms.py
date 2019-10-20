from django import forms


class SolutionForm(forms.Form):

    def __init__(self, solution, **kwargs):
        if solution:
            kwargs['initial'] = {'content': solution.last_changes}
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
