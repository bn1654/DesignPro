from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import AbsUser

class SignUpForm(UserCreationForm):
    FIO = forms.CharField(max_length=255, required=True, help_text='Ваше ФИО')

    class Meta:
        model = AbsUser
        fields = ('FIO', 'username', 'email', 'password1', 'password2', )