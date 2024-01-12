from .news import AllNews
from django.db.models import Q
from tag.models import Tag
from news.models import News
# Tradução
from django.utils import translation
from django.utils.translation import gettext
from utils.mixin import ViewLanguageMixin


class SearchNews(AllNews, ViewLanguageMixin):
    # Permite iniciar algumas informações, um pouco parecido com herença e __init__
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # Pegar o "name" do meu campo search
        # Está na navegação do boostrap
        self.search_term = request.GET.get('q', '').strip()

    def get_queryset(self):
        qs = super().get_queryset()

        # __icontains = Como se fosse o Like
        # Q = Troca para "ou" ao invés de "e"
        qs = qs.filter(Q(title__icontains=self.search_term) |
                       Q(description__icontains=self.search_term),
                       is_published=True).order_by('-id')

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        cd = super().get_context_data(**kwargs)

        # Paginação some o "search_term", criei um cache para isso não acontecer
        # Não muda em nada a paginação, não é obrigatório
        if not self.request.session.get('search_term', ''):
            self.request.session['search_term'] = self.search_term
        cache_profile_term = self.request.session['search_term']

        # Pegar o idioma do navegador da pessoa
        html_language = translation.get_language()

        cd.update({
            'search_term': self.search_term,
            'title': f'Termo da busca = {self.search_term}',
            'post_search_title': True
        })

        return cd


class ViewTag(AllNews, ViewLanguageMixin):
    template_name = 'news/tag.html'

    # Permite iniciar algumas informações, um pouco parecido com herença e __init__
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # Pegar o "name" do meu campo search
        # Está na navegação do boostrap
        self.search_term = request.GET.get('q', '').strip()

    def get_queryset(self):
        qs = super().get_queryset()

        # __icontains = Como se fosse o Like
        # Q = Troca para "ou" ao invés de "e"
        qs = qs.filter(tags__slug=self.kwargs.get('slug'))

        qs = qs.prefetch_related('tags', )

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        cd = super().get_context_data(**kwargs)

        # Paginação some o "search_term", criei um cache para isso não acontecer
        # Não muda em nada a paginação, não é obrigatório
        if not self.request.session.get('search_term', ''):
            self.request.session['search_term'] = self.search_term
        cache_profile_term = self.request.session['search_term']

        # Filtrando minhas tags
        tags = Tag.objects.filter(slug=self.kwargs.get('slug')).first()

        # Traduzir tags
        # Envia uma string
        # Não vou usar no momento
        # tags = gettext('Category')

        # Filtrar notícias com a tag filtrada acima
        news_posts = News.objects.filter(tags__name__icontains=tags)

        # Se não encontrar nenhuma tag, não envio o "search_term"
        post_search_title = True if tags else False

        # Se tag não existir, variável com mensagem de erro
        if not tags:
            tags = 'Não tem nenhuma noticia com esse tag'

        # Pegar o idioma do navegador da pessoa
        # Vou colocar isso na tag html lang
        html_language = translation.get_language()

        cd.update({
            'search_term': tags,
            'title': f'{tags}',
            'post_search_title': post_search_title,
            'posts': news_posts,
            'html_language': html_language
        })

        return cd
