from django import forms


class GroupSearchForm(forms.Form):

    search = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по названию группы',
            'class': 'form-control'
        })
    )