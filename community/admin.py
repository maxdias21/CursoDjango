from django.contrib import admin
from .models import Community
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.

class BlogConfig(SummernoteModelAdmin):
    summernote_fields = ('content',)

    # Serve pra mostrar a lista de campos no display
    list_display = ('id', 'title', 'author', 'is_published')

    # Serve para criar um link, quando eu clicar no link eu abro uma nova guia
    list_display_links = ('id', 'title')

    # Serve para mostrar apenas 10 notícias | Se tiver mais cria uma paginação
    list_per_page = 100

    # Cria um filtro de busca avançado
    list_filter = ('author', 'created_at')

    # Serve para editar algo sem precisar abrir uma nova guia
    list_editable = ('is_published',)

    # Serve pra realizar buscar com os campos selecionados abaixo
    search_fields = ('title', 'author')


admin.site.register(Community, BlogConfig)
