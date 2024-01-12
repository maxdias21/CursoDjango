from community.models import Community
from django.db.models import Q
from authors.models import AuthorRegister
from utils.pagination.pagination import make_pagination
from django.views.generic import ListView
from utils.mixin import ViewLanguageMixin


class SearchCommunityPosts(ListView, ViewLanguageMixin):
    model = Community
    template_name = 'community/search_posts.html'
    ordering = ['-id']

    # Permite iniciar algumas informações, um pouco parecido com herença e __init__
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.search_term = request.GET.get('q', '').strip()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            Q(title__icontains=self.search_term) |
            Q(description__icontains=self.search_term),
            is_published=True).order_by('-id')

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        cd = super().get_context_data(**kwargs)

        # Pegar meu perfil
        profile = AuthorRegister.objects.filter(
            username=self.request.user).first() if self.request.user.is_authenticated else ''

        # Paginação
        page_obj, pagination_range = make_pagination(self.request, self.get_queryset(), 12)

        # Paginação some o "search_term", criei um cache pra isso não acontecer
        # Não muda em nada a paginação, não é obrigatório
        if not self.request.session.get('search_term'):
            self.request.session['search_term'] = self.search_term
        cache_search_term = self.request.session['search_term']

        cd.update({
            'search_term': cache_search_term if cache_search_term else '',
            'posts': page_obj,
            'pagination_range': pagination_range,
            'profile': profile,
            'title': self.search_term
        })

        return cd

