from django.shortcuts import render
from django.contrib.auth.models import User
from .models import News
from django.http import Http404
from django.db.models import Q
from utils.pagination.pagination import make_pagination
from community.models import Community


# Create your views here.

# Página inicial
def news(request):
    # Pegar os 4 últimos usuários registrados
    new_users = User.objects.all().order_by('-id')[0:4]

    # Pegar notícias principais
    first_news = News.objects.filter(is_published=True, type='MainNews').first()
    second_news = News.objects.filter(is_published=True, type='SecondaryNewsTop').first()
    third_news = News.objects.filter(is_published=True, type='SecondaryNewsBottom').first()

    # Pegar notícias da comunidade
    community = Community.objects.filter(is_published=True).order_by('-id')[0:5]

    # Pegar notícias
    posts = News.objects.all().order_by('-id').filter(is_published=True)[0:10]

    return render(request=request, template_name='news/index.html', context={
        'new_users': new_users,
        'news': posts,
        'first_news': first_news,
        'second_news': second_news,
        'third_news': third_news,
        'community': community
    })


# Fim da página inicial

# Visualizar uma notícia específica
def news_view(request, pk):
    # Pegar as notícias
    news = News.objects.get(id=pk)

    # Pegar as últimas 4 notícias
    last_news = News.objects.all().order_by('-id')[0:4]

    return render(request, 'news/news.html', context={
        'post': news,
        'title': news.title,
        'last_news': last_news
    })


# Fim visualizar uma notícia específica

# Todas as notícias
def all_news(request):
    news = News.objects.filter(is_published=True)

    # Paginação
    page_obj, paginator_range = make_pagination(request, news, 10)

    return render(request, 'news/partials/__all_news_or_search.html', context={
        'news': page_obj,
        'pagination_range': paginator_range,
        'title': 'Todas as notícias'
    })


# Fim todas as notícias

# Início buscar notícias "search"
def search(request):
    # Pegar o "name" do meu campo search
    # Está na navegação do boostrap
    search_term = request.GET.get('q', '').strip()

    # Retorna erro 404
    if search_term is None:
        raise Http404()

    # __icontains = Como se fosse o Like
    # Q = Troca para "ou" ao invés de "e"
    news = News.objects.filter(Q(title__icontains=search_term) | Q(description__icontains=search_term),
                               is_published=True).order_by('-id')

    # Paginação some o "search_term", criei um cache pra isso não acontecer
    # Não muda em nada a paginação, não é obrigatório
    if not request.session.get('search_term', ''):
        request.session['search_term'] = search_term
    cache_profile_term = request.session['search_term']

    # Paginação
    page_obj, paginator_range = make_pagination(request, news, 10)

    return render(request, 'news/partials/__all_news_or_search.html', {
        'posts': page_obj,
        'pagination_range': paginator_range,
        'title': f'Termo da busca={search_term}',
        'search_term': cache_profile_term,
        'post_search_title': True
    })

# Fim início buscar notícias "search"
