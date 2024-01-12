from django.views.generic import View
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import Http404


class LogoutView(View):
    def get(self, request):
        raise Http404()

    def post(self, request):
        # Se tentar sair com um usuário diferente, vai dar erro
        if request.POST.get('username') != request.user.username:
            messages.error(request, 'Erro ao sair da conta')
            return redirect('news:news')

        # Logout realizado com sucesso
        messages.success(request, 'Você saiu da sua conta com sucesso!')
        logout(request)
        return redirect('authors:login_view')
