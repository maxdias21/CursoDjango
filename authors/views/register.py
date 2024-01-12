from django.views import View
from django.contrib import messages
from django.shortcuts import redirect, render
from authors.forms import RegisterForm
from utils.mixin import ViewLanguageMixin
from utils.mixin import get_language


class RegisterPerson(View, ViewLanguageMixin):
    # Dispatch é responsável por retornar um http response (get/post)
    # Faz automático, mas posso personalizar
    def dispatch(self, request, *args, **kwargs):
        # Se o usuário estiver logado, redireciono para o perfil dele
        if request.user.is_authenticated:
            return redirect('authors:profile')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # Criar um cache para salvar as informações e não precisar ficar preenchendo o campo toda hora
        register_form_data = self.request.session.get('register_form_data', None)

        # Criar formulário e caso falhe na hora de criar o usuário, os campos vão estar preenchidos
        form = RegisterForm(register_form_data)

        return render(self.request, 'authors/register.html', context={
            'form': form,
            'html_language': get_language()
        })

    def post(self, request):
        # Pegar os campos do formulário
        post = self.request.POST

        # Pegar os dados do formulário e colocar no cache que eu criei no "register_view"
        self.request.session['register_form_data'] = post

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

            messages.success(self.request, 'Seu usuário foi registrado com sucesso!')

            # Deletar o cache | redirecionar para a página de login
            del self.request.session['register_form_data']
            return redirect('authors:login_view')

        return redirect('authors:register_view')
