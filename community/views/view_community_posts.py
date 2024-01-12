from community.models import Community
from authors.models import AuthorRegister
from utils.pagination.pagination import make_pagination
from django.views.generic import ListView
from django.contrib.auth.models import User
from utils.mixin import ViewLanguageMixin


class PostsBase(ListView, ViewLanguageMixin):
    model = Community

    # Permite iniciar algumas informações, um pouco parecido com herença e __init__
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # Pegar meu perfil
        self.profile = AuthorRegister.objects.filter(
            username=request.user).first() if request.user.is_authenticated else ''

    def get_context_data(self, *, object_list=None, **kwargs):
        cd = super().get_context_data(**kwargs)

        # Paginação
        page_obj, pagination_range = make_pagination(self.request, self.get_queryset(), 6)

        cd.update({
            'profile': self.profile,
            'posts': page_obj,
            'pagination_range': pagination_range,
        })

        return cd


class MyPosts(PostsBase):
    template_name = 'community/my_posts.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author=self.request.user, is_published=True).order_by('-id')

        return qs


class AllPersonPosts(PostsBase):
    template_name = 'community/post_person.html'

    # Permite iniciar algumas informações, um pouco parecido com herença e __init__
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # Pegar perfil do usuario que contem os posts
        self.profile_person = AuthorRegister.objects.filter(slug=self.kwargs.get('slug')).first()

        # Pegar a instância do usuário para filtrar o author no queryset
        self.user = User.objects.filter(username=self.profile_person).first()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author=self.user, is_published=True).order_by('-id')

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        cd = super().get_context_data(**kwargs)
        cd.update({
            'user': self.profile_person
        })

        return cd
