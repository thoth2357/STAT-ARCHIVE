from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
import re


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True,widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Matric Number'}))
    password = forms.CharField(max_length=100, required=True,widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Password'}))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Email'}))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Matric Number'}))
    fullname = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Full Name'}))
    password1 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['fullname', 'username', 'email', 'password1']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username
