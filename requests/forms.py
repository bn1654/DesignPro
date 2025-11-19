import os
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import AbsUser, Request, Category
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    FIO = forms.CharField(required=True, help_text='Ваше ФИО, только кириллица, пробелы и дефис', label='ФИО')
    username = forms.CharField(label='Логин', help_text='Ваш логин, только латинница и дефис')
    
    privacy_agreement = forms.BooleanField(label="Согласие на обработку персональных данных", help_text="Для регистрации необходимо дать свое согласие", required=False)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        
        if AbsUser.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким логином уже существует")
        
        if not re.match(r'^[a-z\-]+$', username.lower()):
            raise ValidationError("Логин введен неверно")
        
        return username
    
    def clean_FIO(self):
        FIO = self.cleaned_data['FIO']
            
        if not re.match(r'^[а-я\-\s]+$', FIO.lower()):
            raise ValidationError("ФИО введены неверно")

        return FIO
        
    def clean_email(self):
        email = self.cleaned_data['email']
        
        if AbsUser.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует")
        
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        accept_privacy = cleaned_data.get('privacy_agreement')
        if not accept_privacy:
            raise ValidationError({'privacy_agreement': "Вы должны принять условия пользовательского соглашения"})
        
        return cleaned_data

    class Meta:
        model = AbsUser
        fields = ('FIO', 'username', 'email', 'password1', 'password2', 'privacy_agreement')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')

class RequestCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(label='Категория', queryset=Category.objects.all(), empty_label="Выберете категорию...", widget=forms.Select(attrs={"class": "form-select"}))
    image = forms.ImageField(label='Изображение', required=True)
    
    def clean_image(self):
        image = self.cleaned_data['image']
        ext = os.path.splitext(image.name)[1]
        valid_formats = ['.jpg', '.jpeg', '.png', '.bmp']
        
        if ext not in valid_formats:
            raise ValidationError("Неверное расширение файла")
        
        if image.size > 2*(1024**2):
            raise ValidationError("Файл не должен превышать 2 МБ")
        
        return image
    
    
    
    class Meta:
        model = Request
        fields = ('name','summary','image', 'category')

class RequestStatusAForm(forms.Form):
    commentary = forms.CharField(label="Комментарий", help_text='Для того чтобы изменить статус на "Принято в работу" необходимо оставить комментарий', required=True, widget=forms.TextInput(attrs={"class": "form-control"}))

class RequestStatusСForm(forms.ModelForm):
    completed_image = forms.ImageField(label="Изображение", help_text='Для того чтобы изменить статус на "Выполнено" необходимо добавить изображение выполненной работы', required=True, widget=forms.FileInput(attrs={"class": "form-control"}))
    
    class Meta:
        model = Request
        fields = ['completed_image']