from community.models import Community
from authors.models import AuthorRegister
from utils.pagination.pagination import make_pagination
from django.views.generic import ListView, DetailView
from utils.mixin import ViewLanguageMixin


class CommunityHome(ListView, ViewLanguageMixin):
    model = Community
    template_name = 'community/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True).order_by('-id')[0:12]

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        cd = super().get_context_data(**kwargs)

        # Pegar meu perfil
        profile = AuthorRegister.objects.filter(
            username=self.request.user).first() if self.request.user.is_authenticated else ''

        cd.update({
            'profile': profile
        })

        return cd


class AllPostsCommunity(ListView, ViewLanguageMixin):
    template_name = 'community/partials/__all_news_or_search.html'
    model = Community
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True).order_by('-id')

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        cd = super().get_context_data(**kwargs)

        # Pegar todos os posts
        posts = Community.objects.filter(is_published=True).order_by('-id')

        # Paginação
        page_obj, pagination_range = make_pagination(self.request, posts, 10)

        cd.update({
            'posts': page_obj,
            'pagination_range': pagination_range,
            'title': 'Posts da comunidade',
        })

        return cd


class ViewCommunityPosts(DetailView, ViewLanguageMixin):
    template_name = 'community/post_content.html'
    model = Community
    context_object_name = 'post'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True, slug=self.kwargs.get('slug'))

        return qs

    def get_context_data(self, **kwargs):
        cd = super().get_context_data(**kwargs)

        # Pegar meu perfil
        profile = AuthorRegister.objects.filter(
            username=self.request.user).first() if self.request.user.is_authenticated else ''

        # Verificar/pegar título do post
        title = 'Title is not defined'
        if self.get_queryset()[0].title:
            title = self.get_queryset()[0].title

        cd.update({
            'profile': profile,
            'title': title
        })

        return cd
