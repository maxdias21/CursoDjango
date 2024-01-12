from django.views.generic import ListView
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Q
from utils.pagination.pagination import make_pagination
from authors.models import AuthorRegister
from utils.mixin import ViewLanguageMixin


class SearchPeople(ListView, ViewLanguageMixin):
    template_name = 'community/search_people.html'
    ordering = ['-id']
    model = User

    # Dispatch é responsável por retornar um http response (get/post)
    # Faz automático, mas posso personalizar
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'Antes de procurar algum perfil, faça um registro de graça no nosso site 😄')
            return redirect('authors:register_view')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Pegar o "name" do meu campo search
        search_term = self.request.GET.get('q', '').strip()

        qs = super().get_queryset()

        # __icontains = Como se fosse o Like
        # Q = Troca para "ou" ao invés de "e"
        qs = qs.filter(
            Q(username__icontains=search_term) |
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term),
            Q(profile__is_active=True))


        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        cd = super().get_context_data(**kwargs)
        search_term = self.request.GET.get('q', '').strip()

        # Pegar meu perfil
        profile = AuthorRegister.objects.filter(username=self.request.user).first() if self.request.user.is_authenticated else ''


        # Paginação some o "search_term", criei um cache para isso não acontecer
        # Não muda em nada a paginação, não é obrigatório
        self.request.session['search_term'] = search_term

        # Paginação
        page_obj, pagination_range = make_pagination(self.request, self.get_queryset(), 12)

        cd.update({
            'posts': page_obj,
            'pagination_range': pagination_range,
            'search_term': self.request.session['search_term'],
            'title': search_term,
            'profile': profile
        })

        return cd
