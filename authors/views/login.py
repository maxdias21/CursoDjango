from django.views import View
from django.contrib import messages
from django.shortcuts import reverse, redirect, render
from authors.forms.login import LoginForm
from django.contrib.auth import login, authenticate
from utils.mixin import ViewLanguageMixin
from utils.mixin import get_language


class Login(View, ViewLanguageMixin):
    # Dispatch é responsável por retornar um http response (get/post)
    # Faz automático, mas posso personalizar
    def dispatch(self, request, *args, **kwargs):
        # Se o usuário estiver logado, redireciono para o perfil dele
        if request.user.is_authenticated:
            return redirect('authors:profile')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # Pegar o form login
        form = LoginForm()

        return render(self.request, template_name='authors/login.html', context={
            'form': form,
            'form_action': reverse('authors:login_create'),
            'html_language': get_language()
        })

    def post(self, request):
        # Pegar o formulário
        form = LoginForm(self.request.POST)

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
                messages.success(self.request, 'Usuário logado com sucesso!')
                login(self.request, authenticate_user)

            # Usuário digitou algo errado ou a conta não existe
            else:
                messages.error(self.request, 'Usuário não existe ou a senha está incorreta, verifique suas credenciais')
        # Erro no formulário
        else:
            messages.error(self.request, 'Erro ao enviar o formulário')

        return redirect(reverse('authors:login_view'))
