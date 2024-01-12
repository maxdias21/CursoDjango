from django import forms
from utils.django_forms import add_placeholder, add_label


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Campos
        username_field = self.fields['username']
        password_field = self.fields['password']

        # Adicionar placeholder
        add_placeholder(username_field, 'Digite seu usuário')
        add_placeholder(password_field, 'Digite sua senha')

        # Adicionar label
        add_label(username_field,'Usuário')
        add_label(password_field,'Senha')


    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())
