from django.contrib import admin
from .models import Tag


# Register your models here.


class TagAdmin(admin.ModelAdmin):
    # Serve pra mostrar a lista de campos no display
    list_display = ['id', 'name', 'slug']

    # Permite criar um link, quando eu clicar no link eu abro uma nova guia
    list_display_links = ['id', 'slug']

    # Serve pra realizar buscar com os campos selecionados abaixo
    search_fields = ['id', 'slug', 'name']

    # Permite mostrar apenas 10 notícias | Se tiver mais cria uma paginação
    list_per_page = 10

    # Permite editar algo sem precisar abrir uma nova guia
    list_editable = ('name',)

    # Ordenar, coloquei por id decrescente
    ordering = ['-id']

    # Preenche um campo de forma automática
    # Chave = campo que vai ser preenchido
    # Valor = campo que vai no "slug" - exemplo
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Tag, TagAdmin)
