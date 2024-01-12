from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, CreateProfile
from .models import AuthorRegister
from django.contrib.auth.models import User
from django.db.models import Q
from utils.pagination.pagination import make_pagination

"""
Estou usando Class Base Views, nada aqui está funcionando
Deixei apenas para lembrar quando eu quiser usar function base views :)
"""


# Parte do login
def login_view(request):
    # Verificar se a pessoa está logada, se estiver eu redireciono para o perfil ao invés de redirecionar
    # para a página de login
    if request.user.username:
        return redirect('authors:profile')

    # Pegar o form login
    form = LoginForm()

    return render(request, template_name='authors/login.html', context={
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    # Se tentar acessar com o método GET, levanta o erro 404
    if not request.POST:
        raise Http404()

    # Pegar o formulário
    form = LoginForm(request.POST)

    # Se o formulário for válido, entra no "if"
    # Entrar não significa que vai logar, só que os campos foram preenchidos corretamente
    if form.is_valid():
        # Vou autenticar o usuário | retorna o nome do usuário ou None
        authenticate_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )

        # Se entrar no "if" vai logar o usuário
        if authenticate_user is not None:
            messages.success(request, 'Usuário logado com sucesso!')
            login(request, authenticate_user)

        # Usuário digitou algo errado ou a conta não existe
        else:
            messages.error(request, 'Usuário não existe ou a senha está incorreta, verifique suas credenciais')
    # Erro no formulário
    else:
        messages.error(request, 'Erro ao enviar o formulário')

    return redirect(reverse('authors:login_view'))


# Fim da parte do login


# Início da parte do registro do usuário
def register_view(request):
    # Se o usuário estiver logado, redireciono para o perfil dele
    if request.user.is_authenticated:
        return redirect('authors:profile')

    # Criar um cache para salvar as informações e não precisar ficar preenchendo o campo toda hora
    register_form_data = request.session.get('register_form_data', None)

    # Criar formulário e caso falhe na hora de criar o usuário, os campos vão estar preenchidos
    form = RegisterForm(register_form_data)

    return render(request, 'authors/register.html', context={
        'form': form
    })


def register_create(request):
    # Se tentar acessar com o método GET, levanta o erro 404
    if not request.POST:
        raise Http404()

    # Pegar os campos do formulário
    post = request.POST

    # Pegar os dados do formulário e colocar no cache que eu criei no "register_view"
    request.session['register_form_data'] = post

    # Criar o formulário passando os dados do cache
    form = RegisterForm(post)

    # Se o formulário for válido, entra no "if"
    # Entrar não significa que vai logar, só que os campos foram preenchidos corretamente
    if form.is_valid():
        # Receber as informações do formulário
        # commit = False | para não salvar o formulário, pois vou personalizar alguns campos
        user = form.save(commit=False)

        # Criptografar a senha e salvar
        user.set_password(user.password)
        user.save()

        messages.success(request, 'Seu usuário foi registrado com sucesso!')

        # Deletar o cache | redirecionar para a página de login
        del request.session['register_form_data']
        return redirect('authors:login_view')

    return redirect('authors:register_view')


# Fim da parte do registro do usuário


@login_required(login_url='authors:login_view')
def create_profile_view(request):
    # Criar um cache para salvar as informações e não precisar ficar preenchendo o campo toda hora
    create_form_data = request.session.get('create_form_data', None)

    # Pegar o formulário
    form = CreateProfile(data=create_form_data)

    return render(request, template_name='authors/create_or_edit_profile.html', context={
        'form': form,
        'form_action': reverse('authors:create_profile_create')
    })


# Início da parte da criação do perfil + edição do perfil
@login_required(login_url='authors:login_view')
def create_profile_create(request):
    # Se tentar acessar com o método GET, levanta o erro 404
    if not request.POST:
        raise Http404()

    # Pegar os campos do formulário
    post = request.POST

    # Criar o cache ou atualizar
    request.session['create_form_data'] = post

    # Formulário com o cache
    form = CreateProfile(data=post, files=request.FILES or None)
    print('ok')
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


@login_required(login_url='authors:login_view')
def profile_edit(request):
    # Verificar se o usuário possui um perfil
    profile = AuthorRegister.objects.filter(username=request.user).first()

    # Caso o usuário não tenha criado um perfil, ele será redirecionado para a página de criar perfil
    if not profile:
        messages.warning(request, 'Crie um perfil para criar/publicar conteúdos na categoria community gratuitamente')
        return redirect('authors/create_or_edit_profile.html')

    # Instance serve pra informar que é uma instância de profile, sem ele não dá pra alterar as informações
    # Ele tentaria criar algo novo ao invés de editar
    form = CreateProfile(
        data=request.POST or None,
        instance=profile,
        files=request.FILES or None

    )

    if form.is_valid():
        # Receber as informações do formulário
        # commit = False | para não salvar o formulário, pois vou personalizar alguns campos
        profile = form.save(commit=False)

        # Adicionar o usuário
        profile.username = request.user

        # Salvar o formulário | mensagem de sucesso | redirecionar para o perfil atualizado
        profile.save()
        messages.success(request, 'Perfil editado com sucesso!')
        return redirect('authors:profile')

    return render(request, 'authors/create_or_edit_profile.html', context={
        'form': form,
    })


# Fim da parte da criação do perfil + edição do perfil


# Início da parte do logout
@login_required(login_url='authors:login_view', redirect_field_name='next')
def logout_view(request):
    # Se tentar acessar com o método GET, levanta o erro 404
    if not request.POST:
        messages.error(request, 'Erro ao sair da conta')
        return redirect('news:news')

    # Se tentar sair com um usuário diferente, vai dar erro
    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Erro ao sair da conta')
        return redirect('news:news')

    # Logout realizado com sucesso
    messages.success(request, 'Você saiu da sua conta com sucesso!')
    logout(request)
    return redirect('authors:login_view')


# Fim da parte do logout


# Início da parte da visualização do "meu perfil"
@login_required(login_url='authors:login_view')
def my_profile(request):
    # Verificar se o usuário já possui um perfil
    profile = AuthorRegister.objects.filter(username=request.user).first()

    # Caso não possua um perfil, vá para a página para criar um
    # Sem perfil não entra no my_profile
    if not profile:
        messages.warning(request, 'Você não tem um perfil de usuário, vamos criar um agora...')
        return redirect('authors:create_profile_view')

    return render(request, 'authors/my_profile.html', {
        'profile': profile,
        'title': f'{request.user.first_name} {request.user.last_name}'
    })


# Fim da parte da visualização do "meu perfil"

# Início da parte da visualização do perfil dos usuários
def profile_complete_person(request, id):
    if not request.user.is_authenticated:
        messages.info(request, 'Para visualizar algum perfil, faça um registro no nosso site, é de graça 😄')
        return redirect('authors:register_view')

    user = User.objects.filter(id=id).first()

    profile = AuthorRegister.objects.filter(username=user).first()

    if not profile:
        messages.error(request, 'Erro ao acessar o perfil selecionado')
        return redirect('authors:profile_person')

    if profile.profile_status == 'Privado':
        messages.error(request, 'O perfil selecionado é privado.')
        return redirect('community:community')

    if profile.is_active == False:
        messages.error(request, 'O perfil do usuário se encontra indisponível no momento.')
        return redirect('community:community')

    if user == request.user:
        messages.success(request, 'Você está vendo seu perfil agora')

    return render(request, 'authors/profile_person.html', {
        'profile': profile,
        'user': user
    })


# Fim da parte da visualização do perfil dos usuários

# Parte da busca "perfil do usuário"
def search_perfil_person(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Antes de procurar algum perfil, faça um registro de graça no nosso site 😄')
        return redirect('authors:register_view')

    # Pegar o "name" do meu campo search
    search_term = request.GET.get('q', '').strip()

    # Pegar meu perfil
    profile = AuthorRegister.objects.filter(username=request.user).first() if request.user.is_authenticated else ''

    # __icontains = Como se fosse o Like
    # Q = Troca para "ou" ao invés de "e"
    profiles = User.objects.filter(
        Q(username__icontains=search_term)
        | Q(first_name__icontains=search_term)
        | Q(last_name__icontains=search_term),
        Q(profile__is_active=True)
    )

    # Paginação some o "search_term", criei um cache pra isso não acontecer
    # Não muda em nada a paginação, não é obrigatório
    if not request.session['search_term']:
        request.session['search_term'] = search_term
    cache_profile_term = request.session['search_term']

    # Paginação
    page_obj, pagination_range = make_pagination(request, profiles, 12)

    return render(request, 'community/search_people.html', {
        'posts': page_obj,
        'pagination_range': pagination_range,
        'search_term': cache_profile_term,
        'profile': profile,
        'title': search_term
    })

# Fim da busca "perfil do usuário"

# Parte da busca "posts da comunidade"
