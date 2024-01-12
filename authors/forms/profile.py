from django.forms import ModelForm
from authors.models import AuthorRegister
from utils.django_forms import add_placeholder, add_label
from collections import defaultdict
from django.core.exceptions import ValidationError
from django.contrib import messages
from django import forms


class CreateProfile(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Campos
        phone_number_field = self.fields['phone_number']
        age_field = self.fields['age']
        description_field = self.fields['description']
        marital_status = self.fields['marital_status']
        profile_status = self.fields['profile_status']

        # Adicionar label
        add_label(phone_number_field, 'Telefone')
        add_label(age_field, 'Idade')
        add_label(description_field, 'Descrição')
        add_label(profile_status, 'Privacidade do perfil')

        # Adicionar placeholders
        add_placeholder(phone_number_field, 'Seu número de telefone')
        add_placeholder(age_field, 'Digite sua idade')
        add_placeholder(description_field, 'Um pouco sobre você... (máximo 500 caracteres)')

        # Adicionar erros
        phone_number_field.error_messages = {
            'required': 'Campo telefone é obrigatório',
            'max_length': 'Máximo de caracteres permitidos é 11',
            'min_length':'Mínimo de caracteres permitidos é 11'
        }

        age_field.error_messages = {
            'required': 'Campo idade é obrigatório',
        }

        description_field.error_messages = {
            'required': 'Campo descrição é obrigatório',
            'max_length': 'Máximo de caracteres permitidos é 500',
            'min_length': 'Mínimo de caracteres permitidos é 10'
        }

        marital_status.error_messages = {
            'required': 'Campo estado civil é obrigatório',
            'max_length': 'Máximo de caracteres permitidos é 10',
            'min_length': 'Mínimo de caracteres permitidos é 1'
        }

        profile_status.error_messages = {
            'required': 'Campo estado civil é obrigatório',
            'max_length': 'Máximo de caracteres permitidos é 10',
            'min_length': 'Mínimo de caracteres permitidos é 1'
        }



    # Adicionar Max Length | Min Length
    phone_number = forms.CharField(max_length=11, min_length=11)
    description = forms.CharField(max_length=500, min_length=10)

    class Meta:
        model = AuthorRegister
        fields = ('age', 'hometown', 'current_city', 'marital_status',
                  'phone_number', 'description', 'photo', 'profile_status')

    def clean(self):
        # Criar um dicionário que contém dicionários
        # Toda vez que eu usar isso ele cria um dicionário com uma lista
        # Envio todos os erros ao invés de ficar a colocar raise ValidationError para cada campo individual
        errors = defaultdict(list)

        # Pegar todos os campos
        cleaned_data = self.cleaned_data

        # Pegar campos individuais
        age = cleaned_data.get('age')
        hometown = cleaned_data.get('hometown')
        current_city = cleaned_data.get('current_city')
        phone_number = cleaned_data.get('phone_number')
        description = cleaned_data.get('description')

        try:
            if age < 0 or age > 130:
                errors['age'].append('Idade inválida, tente novamente')

            if len(hometown) < 3:
                errors['hometown'].append('Digite em qual cidade você nasceu')

            if len(current_city) < 3:
                errors['current_city'].append('Digite em qual cidade você mora atualmente')

            if len(str(phone_number)) < 10 or len(str(phone_number)) > 11:
                errors['phone_number'].append('Digite seu número de telefone com + DDD')

            if not (str(phone_number).isnumeric()):
                errors['phone_number'].append('Apenas números entre [0-9], sem pontos, vírgulas ou parênteses')

            if len(description) < 10:
                errors['description'].append('Digite algo simples sobre você, no mínimo 10 caracteres e no máximo 500')
        except:
            pass

        if errors:
            raise ValidationError(errors)

