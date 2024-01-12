from django.shortcuts import render, redirect, reverse
from community.forms.comunity_create_post import ComunityCreatePost
from django.contrib import messages
from authors.models import AuthorRegister
from django.views import View
from utils.mixin import ViewLanguageMixin
from utils.mixin import get_language


class CreateCommunityPost(View, ViewLanguageMixin):
    # Permite iniciar algumas informações, um pouco parecido com herença e __init__
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # Criar um cache para salvar as informações e não precisar ficar a preencher o campo toda hora
        create_form_data = request.session.get('create_form_data', None)

        # Pegar o formulário
        self.form = ComunityCreatePost(data=create_form_data) if request.user.is_authenticated else ''

        # Verificar se o usuário tem um perfil
        self.profile = AuthorRegister.objects.filter(username=request.user).first()

    # Dispatch é responsável por retornar um http response (get/post)
    # Faz automático, mas posso personalizar
    def dispatch(self, request, *args, **kwargs):
        # Se não tiver perfil, retorna para a página de criar um perfil
        if not self.profile:
            messages.error(request, 'Para criar posts para a comunidade, crie um perfil antes :)')
            return redirect('authors:register_view')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'community/create_post.html', context={
            'form': self.form,
            'form_action': reverse('community:create_community_post_create'),
            'profile': self.profile,
            'html_language': get_language()
        })

    def post(self, request):
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
        return redirect('community:create_community_post_view')
