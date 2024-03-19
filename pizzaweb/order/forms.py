from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'
    class Meta:
        model = Product
        fields = ['title','price','slug','desc','photo','cat']

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',widget=forms.TextInput(attrs={}))
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={}))

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин',widget=forms.TextInput(attrs={}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={}))
    password1 = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={}))
    password2 = forms.CharField(label='Повтор пароля',widget=forms.PasswordInput(attrs={}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class AboutForm(forms.Form):
    from_email = forms.EmailField(label='Email', required=True)
    subject = forms.CharField(label='Тема', required=True)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea, required=True)
