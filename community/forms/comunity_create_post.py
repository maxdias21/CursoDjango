from django.forms import ModelForm
from community.models import Community
from utils.django_forms import add_placeholder, add_help_text
from django.core.validators import ValidationError
from django import forms
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget


class ComunityCreatePost(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pegar campos
        content_field = self.fields['content']

        # Adicionar placeholder
        add_placeholder(self.fields['content'], 'Digite o conteúdo principal do seu post')

        # Adicionar texto de ajuda
        add_help_text(content_field, 'Tags HTML e comandos JS não são suportados, ficam em formato de texto')

    title = forms.CharField(required=True, max_length=100, min_length=5,
                            label='Título do post',
                            error_messages={
                                'required': 'Título não pode ficar em branco',
                                'max_length': 'Máximo de caracteres permitido é 100',
                                'min_length': f'Título deve conter 5 caracteres ou mais'
                            },
                            widget=forms.TextInput(attrs={
                                'placeholder': 'Digite o título do seu post'
                            })
                            )

    description = forms.CharField(required=True, max_length=100, min_length=10,
                                  label='Descrição',
                                  error_messages={
                                      'required': 'Descrição não pode ficar em branco',
                                      'max_length': 'Máximo de caracteres permitido é 100',
                                      'min_length': 'Descrição deve conter 10 caracteres ou mais'
                                  },
                                  widget=forms.TextInput(attrs={
                                      'placeholder': 'Digite uma descrição curta e bem explicativa'
                                  })
                                  )

    content = SummernoteTextField()

    class Meta:
        model = Community
        fields = ['title', 'description', 'content', 'image']
        # SummerNote
        widgets = {
            'content': SummernoteWidget(),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        if (len(str(cleaned_data.get('content')))) < 10:
            raise ValidationError({'content': 'Conteúdo principal deve ter no mínimo 10 caracteres'})
