from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthorsTestLogout(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        username = 'MyUsername'
        password = 'Password123'

        # Criar um usuário apenas com usuário | senha
        User.objects.create_user(username=username, password=password)

        # Logar o usuário
        self.client.login(username=username, password=password)

        # Http response | status code e várias outras coisas...
        response = self.client.get(reverse('authors:logout'), follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn('Erro ao sair da conta', content)

    def test_user_tries_to_logout_another_user(self):
        username = 'MyUsername'
        password = 'Password123'

        # Criar um usuário apenas com usuário | senha
        User.objects.create_user(username=username, password=password)

        # Logar o usuário
        self.client.login(username=username, password=password)

        # Http response | status code e várias outras coisas...
        # "Data" - criei um parâmetro para cair numa asserção na minha view "logout_view"
        response = self.client.post(reverse('authors:logout'), follow=True, data={
            'username': 'AnotherUsername'
        })

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn('Erro ao sair da conta', content)

    def test_user_can_logout_successfully(self):
        username = 'MyUsername'
        password = 'Password123'

        # Criar um usuário apenas com usuário | senha
        user = User.objects.create_user(username=username, password=password)

        # Logar o usuário
        self.client.login(username=username, password=password)

        # Http response | status code e várias outras coisas...
        response = self.client.post(reverse('authors:logout'), follow=True, data={
            'username': username
        })

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn('Você saiu da sua conta com sucesso!', content)
