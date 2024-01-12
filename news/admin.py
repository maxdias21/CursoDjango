from django.contrib import admin
from .models import News
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.contenttypes.admin import GenericStackedInline
from tag.models import Tag


# Register your models here.

# Em news, quando eu criar uma notícia, ele coloca um campo extra de tag
# Ele adiciona na minha notícia e faz a ligação de um pra muitos
class TagInline(GenericStackedInline):
    model = Tag
    fields = ['name']
    extra = 1


class SummerNoteContent(SummernoteModelAdmin):
    summernote_fields = ('content',)

    # Serve pra mostrar a lista de campos no display
    list_display = ('id', 'title', 'is_published', 'author', 'slug')

    # Serve pra realizar buscar com os campos selecionados abaixo
    search_fields = ('id', 'title', 'author', 'description', 'created_at')

    # Permite editar algo sem precisar abrir uma nova guia
    list_editable = ('is_published',)

    # Permite mostrar apenas 10 notícias | Se tiver mais cria uma paginação
    list_per_page = 10

    # Permite criar um link, quando eu clicar no link eu abro uma nova guia
    list_display_links = ('id', 'title')

    # Cria um filtro de busca avançado
    list_filter = ('author', 'created_at')

    # Preenche um campo de forma automática
    # Chave = campo que vai ser preenchido
    # Valor = campo que vai no "slug" - exemplo
    prepopulated_fields = {'slug': ('title',)}

    # Comentei aqui pois não estou usando ContentTypes e sim ManyToMany
    # O campo extra (classe (TagInline) logo acima com a explicação)
    # inlines = [TagInline]


    # Só funciona para chaves estrangeiras
    # Consigo fazer buscas
    autocomplete_fields = ('tags',)


admin.site.register(News, SummerNoteContent)
