from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    birth_date = forms.DateField(required=True, help_text='Формат: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'birth_date', 'password1', 'password2', )
