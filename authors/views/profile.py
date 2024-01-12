from django.views import View
from django.views.generic import DetailView
from django.contrib import messages
from django.shortcuts import reverse, redirect, render
from authors.models import AuthorRegister
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from authors.forms.profile import CreateProfile
from utils.mixin import ViewLanguageMixin
from utils.mixin import get_language


# Início criar perfil
@method_decorator(login_required(login_url='authors:login_view', redirect_field_name='next'), name='dispatch')
class CreatePersonProfile(View, ViewLanguageMixin):
    def get(self, request):
        # Criar um cache para salvar as informações e não precisar ficar a preencher o campo toda hora
        create_form_data = request.session.get('create_form_data', None)

        # Pegar o formulário
        form = CreateProfile(data=create_form_data)

        return render(request, template_name='authors/create_or_edit_profile.html', context={
            'form': form,
            'form_action': reverse('authors:create_profile_create'),
            'html_language': get_language()
        })

    def post(self, request):
        # Pegar os campos do formulário
        post = request.POST

        # Criar o cache ou atualizar
        request.session['create_form_data'] = post

        # Formulário com o cache
        form = CreateProfile(data=post, files=request.FILES or None)

        if form.is_valid():
            # Receber as informações do formulário
            # commit = False | para não salvar o formulário, pois vou personalizar alguns campos
            author = form.save(commit=False)

            # Adicionar o usuário
            author.username = request.user

            # Ativar usuário
            author.is_active = True

            # Salvar o formulário | mensagem de sucesso | redirecionar para o perfil atualizado
            form.save()
            messages.success(request, 'Perfil alterado com sucesso!')

            # Apagar cache
            del request.session['create_form_data']
            return redirect('authors:profile')

        return redirect('authors:create_profile_view')


# Fim parte criar perfil


# Início editar/visualizar perfil
"""
Parte de editar perfil e visualizar "meu" perfil
Ambos herdam da classe ProfileBase
"""


@method_decorator(login_required(login_url='news:news'), name='dispatch')
class ProfileBase(View, ViewLanguageMixin):
    # Permite iniciar algumas informações, um pouco parecido com herença e __init__
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # Verificar se o usuário possui um perfil
        # Se não tiver eu retorno (se não dá erro no "instance")
        # Ele vai direto pro dispatch caso não esteja logado
        if request.user.is_authenticated:
            self.profile = AuthorRegister.objects.filter(username=request.user).first()
        else:
            return

        # Instance permite informar que é uma instância de profile, sem ele não dá para alterar as informações
        # Ele tentaria criar algo novo ao invés de editar
        self.form = CreateProfile(
            data=request.POST or None,
            instance=self.profile,
            files=request.FILES or None
        )

    # Dispatch é responsável por retornar um http response (get/post)
    # Faz automático, mas posso personalizar
    def dispatch(self, request, *args, **kwargs):
        if not self.profile:
            messages.error(request, 'Você não possui um perfil')
            return redirect('authors:create_profile_view')

        return super().dispatch(request, *args, **kwargs)


class EditPersonProfile(ProfileBase):
    def get(self, request):
        return render(request, 'authors/create_or_edit_profile.html', context={
            'form': self.form,
            'html_language': get_language()
        })

    def post(self, request):
        if self.form.is_valid():
            # Receber as informações do formulário
            # commit = False | para não salvar o formulário, pois vou personalizar alguns campos
            profile = self.form.save(commit=False)

            # Adicionar o usuário
            profile.username = request.user

            # Salvar o formulário | mensagem de sucesso | redirecionar para o perfil atualizado
            profile.save()
            messages.success(request, 'Perfil editado com sucesso!')
            return redirect('authors:profile')

        return render(request, 'authors/create_or_edit_profile.html', context={
            'form': self.form,
        })


class ProfilePerson(ProfileBase, ViewLanguageMixin):
    def get(self, request):
        return render(request, 'authors/my_profile.html', {
            'profile': self.profile,
            'title': f'{request.user.first_name} {request.user.last_name}',
            'html_language': get_language()
        })


class ViewSomeonePerson(DetailView, ViewLanguageMixin):
    model = AuthorRegister
    context_object_name = 'profile'
    template_name = 'authors/profile_person.html'

    # Dispatch é responsável por retornar um http response (get/post)
    # Faz automático, mas posso personalizar
    def dispatch(self, request, *args, **kwargs):
        # Verificar se o usuário está logado
        if not request.user.is_authenticated:
            messages.info(request, 'Crie uma conta gratuitamente no nosso site antes de visualizar um perfil')
            return redirect('authors:register_view')

        # Verificar se o "id" selecionado possui um perfil ativo
        profile = AuthorRegister.objects.filter(slug=kwargs.get('slug')).first()

        # Se o usuário não tiver criado um perfil não tem como visitar
        if not profile:
            messages.error(request, 'Usuário não criou um perfil')
            return redirect('authors:profile_person')

        # Se o perfil for privado, não tem como visitar
        if profile.profile_status == 'Privado':
            messages.error(request, 'O perfil selecionado é privado.')
            return redirect('community:community')

        # Se o perfil for banido/desativado, não tem como visitar
        if not profile.is_active:
            messages.error(request, 'O perfil do usuário se encontra indisponível no momento.')
            return redirect('community:community')

        # Se o perfil selecionado for o da pessoa logada, entra nessa parte
        if profile.username == request.user:
            messages.success(request, 'Você está vendo seu perfil agora')
            return redirect('authors:profile')

        return super().dispatch(request, *args, **kwargs)

# Fim editar/visualizar perfil
