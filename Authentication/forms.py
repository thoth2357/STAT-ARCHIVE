from django import forms
import re

class MatricField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regex = r'^sta/\d{2}/\d{4}$'
        self.error_messages['invalid'] = 'Enter a valid username in the format of sta/**/****'

    def to_python(self, value):
        value = super().to_python(value)
        if value:
            if not re.match(self.regex, value):
                raise forms.ValidationError(self.error_messages['invalid'])
        return value


class LoginForm(forms.Form):
    username = MatricField(max_length=150, required=True,widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Matric Number'}))
    password = forms.CharField(max_length=8, required=True,widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Password'}))
