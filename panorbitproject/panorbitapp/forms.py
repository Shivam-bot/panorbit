from django import forms

from panorbitapp.models import CustomUser


class UserForm(forms.ModelForm):
    save_try = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender', 'email', 'mob_no', 'save_try']


