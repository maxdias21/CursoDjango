from django.shortcuts import render, redirect, reverse
from .models import Community
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms.comunity_create_post import ComunityCreatePost
from django.contrib import messages
from authors.models import AuthorRegister
from utils.pagination.pagination import make_pagination
from django.contrib.auth.models import User


# Página inicial + visualizar um post específico

def comunity(request):
    # Pegar os posts para mostrar na página inicial do community
    post = Community.objects.filter(is_published=True).order_by('-id')[0:8]

    # Pegar meu perfil
    profile = AuthorRegister.objects.filter(username=request.user).first() if request.user.is_authenticated else ''

    return render(request, template_name='community/index.html', context={
        'posts': post,
        'profile': profile
    })


def comunity_view(request, id):
    # Pegar o post
    post = Community.objects.filter(is_published=True, id=id).first()

    # Se o post não existir, retornar 404
    if not post:
        raise Http404()

    # Pegar meu perfil
    profile = AuthorRegister.objects.filter(username=request.user).first() if request.user.is_authenticated else ''

    return render(request, 'community/post_content.html', context={
        'post': post,
        'profile': profile,
        'title': post.title
    })


# Fim página inicial + visualizar um post específico

# Visualizar todos os posts

def all_posts(request):
    # Pegar todos os posts
    posts = Community.objects.filter(is_published=True).order_by('-id')

    # Paginação
    page_obj, pagination_range = make_pagination(request, posts, 10)

    return render(request, 'community/partials/__all_news_or_search.html', {
        'posts': page_obj,
        'pagination_range': pagination_range,
        'title': 'Posts da comunidade'
    })


# Fim visualizar todos os posts

# Criar posts
@login_required(redirect_field_name='authors:register_view')
def create_comunity_post_view(request):
    # Verificar se o usuário tem um perfil
    profile = AuthorRegister.objects.filter(username=request.user).first()

    # Se não tiver perfil, retorna para a página de criar um perfil
    if not profile:
        messages.error(request, 'Para criar posts para a comunidade, crie um perfil antes :)')
        return redirect('authors:register_view')

    # Criar um cache para salvar as informações e não precisar ficar preenchendo o campo toda hora
    create_form_data = request.session.get('create_form_data', None)

    # Pegar o formulário
    form = ComunityCreatePost(data=create_form_data) if request.user.is_authenticated else ''

    # Pegar meu perfil
    profile = AuthorRegister.objects.filter(username=request.user).first() if request.user.is_authenticated else ''

    return render(request, 'community/create_post.html', context={
        'form': form,
        'form_action': reverse('community:create_comunity_post_create'),
        'profile': profile
    })


@login_required(redirect_field_name='authors:register_view')
def create_comunity_post_create(request):
    # Se tentar acessar com o método GET, levanta o erro 404
    if not request.POST:
        raise Http404()

    # Pegar os campos do formulário
    post = request.POST

    # Criar o cache ou atualizar
    request.session['create_form_data'] = post

    # Formulário com o cache
    form = ComunityCreatePost(data=post, files=request.FILES or None)

    if form.is_valid():
        # Receber as informações do formulário
        # commit = False | para não salvar o formulário, pois vou personalizar alguns campos
        author = form.save(commit=False)

        # Adicionar autor do post
        author.author = request.user

        # Salvar o formulário | mensagem de sucesso | redirecionar para o perfil atualizado
        form.save()
        messages.success(request,
                         'Seu post foi enviado para análise, vamos analisar e '
                         'enviar o resultado para você por email')
        del request.session['create_form_data']
        return redirect('community:community')

    messages.error(request, 'Erro ao enviar o seu post, revise os erros abaixo')
    return redirect('community:create_comunity_post_view', )


# Fim Criar posts

# Visualizar "meus posts"

@login_required(login_url='authors:login_view')
def my_posts(request):
    # Pegar todos os posts do usuário
    posts = Community.objects.filter(author=request.user, is_published=True).order_by('-id')

    # Pegar meu perfil
    profile = AuthorRegister.objects.filter(username=request.user).first() if request.user.is_authenticated else ''

    # Paginação
    page_obj, pagination_range = make_pagination(request, posts, 6)

    return render(request, 'community/my_posts.html', {
        'posts': page_obj,
        'pagination_range': pagination_range,
        'profile': profile
    })


# Fim visualizar "meus posts"

# Visualizar post de um autor
@login_required(login_url='authors:login_view')
def post_people(request, id):
    # Pegar perfil do usuario que contem os posts
    profile_person = AuthorRegister.objects.filter(pk=id).first()

    # Pegar todos os posts do usuário
    posts = Community.objects.filter(author=profile_person.username, is_published=True)

    # Pegar meu perfil
    profile = AuthorRegister.objects.filter(username=request.user).first() if request.user.is_authenticated else ''

    # Paginação
    page_obj, pagination_range = make_pagination(request, posts, 6)

    return render(request, 'community/post_person.html', {
        'posts': page_obj,
        'pagination_range': pagination_range,
        'profile': profile,
        'user': profile_person
    })


# Fim visualizar post de um autor

# Deletar post
@login_required(login_url='authors:login_view')
def delete_post(request, id):
    # Se tentar acessar com o método GET, levanta o erro 404
    if not request.POST:
        raise Http404()

    # Pegar dados do site + id para apagar o post
    # id está em um input "hidden"
    post = request.POST
    id = post.get('id')

    # Pegar post
    post = Community.objects.filter(id=id, author=request.user).first()

    if not post:
        messages.error(request, 'Erro ao deletar o post, tente novamente mais tarde')
        return redirect('community:community')

    # Deletar post
    post.delete()

    messages.success(request, 'Post deletado com sucesso!')
    return redirect(reverse('community:my_posts'))


# Fim deletar post

# Início da busca "posts da comunidade"
def search_posts_cominuty(request):
    search_term = request.GET.get('q', '').strip()

    # Pegar posts filtrados
    posts = Community.objects.filter(
        Q(title__icontains=search_term)
        | Q(description__icontains=search_term),
        is_published=True
    ).order_by('-id')

    # Pegar meu perfil
    profile = AuthorRegister.objects.filter(username=request.user).first() if request.user.is_authenticated else ''

    # Paginação some o "search_term", criei um cache pra isso não acontecer
    # Não muda em nada a paginação, não é obrigatório
    if not request.session.get('search_term'):
        request.session['search_term'] = search_term
    cache_search_term = request.session['search_term']

    # Paginação
    page_obj, pagination_range = make_pagination(request, posts, 12)

    return render(request, 'community/search_posts.html', {
        'search_term': cache_search_term if cache_search_term else '',
        'posts': page_obj,
        'pagination_range': pagination_range,
        'profile': profile,
        'title': search_term
    })

# Fim da busca "posts da comunidade"
