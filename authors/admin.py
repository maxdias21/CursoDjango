from django.contrib import admin
from .models import AuthorRegister


# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id','username','phone_number','current_city','hometown','marital_status')

    # Serve pra realizar buscar com os campos selecionados abaixo
    search_fields = ('id', 'username', 'current_city', 'hometown', 'phone_number', 'marital_status')

    # Serve para mostrar apenas 10 perfis de usuário | Se tiver mais cria uma paginação
    list_per_page = 10

    # Serve para criar um link, quando eu clicar no link eu abro uma nova guia
    list_display_links = ('id', 'username')

    # Cria um filtro de busca avançado
    list_filter = ('current_city','hometown','marital_status')



admin.site.register(AuthorRegister,AuthorAdmin)
