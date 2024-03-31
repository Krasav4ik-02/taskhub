from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from manager.models import User


class CustomManagerCreationForm(UserCreationForm):
    exclude_company_identifier = False

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'email',
            'first_name',
            'last_name',
            'name_company',
            'company_identifier',
            'bin',
            'role',
            'data_joined_to_work',

        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'style': "width: 200px",
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': "width: 200px",
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': "width: 200px",
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': "width: 200px",
            }),
            'company_identifier': forms.TextInput(attrs={
                'class': 'form-control',  # Если нужно скрыть, замените на forms.HiddenInput()
                'style': "width: 200px",
            }),
        }

    def __init__(self, *args, **kwargs):
        self.exclude_company_identifier = kwargs.pop('exclude_company_identifier', False)
        super().__init__(*args, **kwargs)

        if self.exclude_company_identifier:
            self.fields.pop('company_identifier')
            self.exclude = ('company_identifier',)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
