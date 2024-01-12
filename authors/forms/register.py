from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from utils.django_forms import add_placeholder, add_label
from django.core.exceptions import ValidationError


class RegisterForm(ModelForm):
    username = forms.CharField(required=True, max_length=20, min_length=4,
                               label='Usuário',
                               error_messages={
                                   'required': 'Digite um usuário válido',
                                   'max_length': 'Máximo de caracteres permitido é 20',
                                   'min_length': 'Usuário deve conter 4 caracteres ou mais',
                               },
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Digite um nome de usuário válido',
                               }),
                               help_text='Usuário não vai poder ser alterado futuramente'
                               )

    email = forms.CharField(required=True, max_length=100, min_length=5,
                               label='Email',
                               error_messages={
                                   'required': 'Digite um email válido',
                                   'max_length': 'Máximo de caracteres permitido é 100',
                                   'min_length': 'Email deve conter 5 caracteres ou mais'
                               },
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Digite um email válido'
                               }),
                               help_text='Email não vai poder ser alterado futuramente'
                               )

    first_name = forms.CharField(required=True, max_length=100, min_length=1,
                               label='Nome',
                               error_messages={
                                   'required': 'Digite seu nome',
                                   'max_length': 'Máximo de caracteres permitido é 100',
                                   'min_length': 'Seu nome deve conter 1 caracteres ou mais'
                               },
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Seu nome'
                               }),
                               help_text='Nome não vai poder ser alterado futuramente'
                               )

    last_name = forms.CharField(required=True, max_length=100, min_length=1,
                               label='Sobrenome',
                               error_messages={
                                   'required': 'Digite seu sobrenome',
                                   'max_length': 'Máximo de caracteres permitido é 100',
                                   'min_length': 'Seu sobrenome deve conter 1 caracteres ou mais'
                               },
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Seu sobrenome'
                               }),
                               help_text='Sobrenome não vai poder ser alterado futuramente'
                               )

    password = forms.CharField(required=True, max_length=50, min_length=6,
                               label='Senha',
                               error_messages={
                                   'required': 'Digite uma senha',
                                   'max_length': 'Máximo de caracteres permitido é 50',
                                   'min_length': 'Senha deve conter 6 caracteres ou mais'
                               },
                               widget=forms.PasswordInput(
                                   attrs={
                                       'placeholder': 'Crie uma senha'
                                   }
                               ))

    password2 = forms.CharField(required=True, max_length=50, min_length=6,
                                label='Repita sua senha',
                                error_messages={
                                    'required': 'Digite uma senha',
                                    'max_length': 'Máximo de caracteres permitido é 50',
                                    'min_length': 'Senha deve conter 6 caracteres ou mais'
                                },
                                widget=forms.PasswordInput(
                                    attrs={
                                        'placeholder': 'Repita sua senha'
                                    }
                                ))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    # Validação de erros

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise ValidationError('Email já cadastrado', code='invalid')

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username','')
        username_exists = User.objects.filter(username=username).exists()

        if username_exists:
            raise ValidationError('Usuário já cadastrado', code='invalid')

        return username



    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        password_input = cleaned_data.get('password')
        password_input2 = cleaned_data.get('password2')

        if password_input != password_input2:
            raise ValidationError({
                'password': 'Senhas precisam ser iguais',
                'password2': 'Senhas precisam ser iguais',
            })
