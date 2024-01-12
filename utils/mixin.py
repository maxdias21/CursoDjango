# Tradução
from django.utils import translation
from django.views.generic.base import ContextMixin




class ViewLanguageMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        cd = super().get_context_data(**kwargs)

        # Pegar o idioma do navegador da pessoa
        # Vou colocar isso na tag html lang
        html_language = translation.get_language()

        cd.update({'html_language': html_language})

        return cd

def get_language():
    html_language = translation.get_language()
    return html_language
