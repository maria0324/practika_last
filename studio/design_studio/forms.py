import re
from django.core.exceptions import ValidationError
from .models import AdvUser, Request
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = AdvUser
        fields = ('name', 'username', 'email', 'password1', 'password2', 'is_activated')

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[а-яА-Я\s-]+$', name):
            raise ValidationError("ФИО может содержать только кириллицу, дефис и пробелы. ")
        return name

    def clean_login(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z\s-]+$', username):
            raise ValidationError("Логин может содержать только латиницу и дефис. ")
        if AdvUser.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким логином уже существует. ")
        return username

class CreateRequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ('request_name', 'description', 'category', 'photo_of_room')



