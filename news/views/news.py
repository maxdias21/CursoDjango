from django.views.generic import ListView, DetailView
from news.models import News
from utils.pagination.pagination import make_pagination
from community.models import Community
from authors.models import AuthorRegister
from utils.mixin import ViewLanguageMixin




class NewsView(ListView, ViewLanguageMixin):
    model = News
    context_object_name = 'news'
    template_name = 'news/index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True).order_by('-id')
        qs = qs.select_related('author')

        return qs[0:8]

    def get_context_data(self, **kwargs):
        cd = super().get_context_data(**kwargs)

        # Pegar os 4 últimos usuários registrados
        new_users = AuthorRegister.objects.filter(profile_status='Público', is_active=True).order_by('-id')[0:4]

        # Pegar notícias da comunidade
        comunity = Community.objects.filter(is_published=True).order_by('-id')[0:5]

        # Pegar notícias principais
        first_news = News.objects.filter(is_published=True, type='MainNews').first()
        second_news = News.objects.filter(is_published=True, type='SecondaryNewsTop').first()
        third_news = News.objects.filter(is_published=True, type='SecondaryNewsBottom').first()

        cd.update({
            'new_users': new_users,
            'first_news': first_news,
            'second_news': second_news,
            'third_news': third_news,
            'community': comunity,
        })

        return cd


class ReadNews(DetailView, ViewLanguageMixin):
    template_name = 'news/news.html'
    context_object_name = 'post'
    model = News

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(slug=self.kwargs.get('slug'))

        return qs

    def get_context_data(self, **kwargs):
        cd = super().get_context_data(**kwargs)

        # Pegar as últimas 4 notícias
        last_news = News.objects.all().order_by('-id')[0:4]

        # Pegar título
        title = self.get_queryset()[0].title[0:20].lower() + '...'

        cd.update({
            'last_news': last_news,
            'title': title if title else ''
        })

        return cd


class AllNews(ListView, ViewLanguageMixin):
    template_name = 'news/partials/__all_news_or_search.html'
    model = News

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True).order_by('-id')

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        cd = super().get_context_data(**kwargs)

        # Paginação
        page_obj, paginator_range = make_pagination(self.request, self.get_queryset(), 10)

        cd.update({
            'posts': page_obj,
            'pagination_range': paginator_range,
            'title': 'Todas as notícias'
        })

        return cd
