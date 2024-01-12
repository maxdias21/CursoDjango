from tests.functional_tests.authors.test.base import AuthorBaseTest
from django.urls import reverse
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from time import sleep


class AuthorsLoginTest(AuthorBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        username = 'MaxLoginTest'
        password = 'MaxLoginSenha'

        # URL inicial
        self.browser.get(self.live_server_url + reverse('authors:login_view'))
        sleep(15)
        # Criar usuário
        user = User.objects.create_user(username=username, password=password)

        # Selecionar formulário
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Selecionar input username
        username_field = form.find_element(By.XPATH, '//input[@placeholder="Digite seu usuário"]')

        # Enviar caracteres para o campo username
        username_field.send_keys(username)

        # Selecionar input password
        password_field = form.find_element(By.XPATH, '//input[@placeholder="Digite sua senha"]')

        # Enviar caracteres para o campo password
        password_field.send_keys(password)

        # Clicar no botão que contém o type submit
        form.submit()

        # A página mudou quando clicou em "form.submit()", pegar formulário novamente
        form = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Usuário logado com sucesso!', form)

    def test_login_create_raises_404_if_not_post_method(self):
        # URL inicial
        self.browser.get(self.live_server_url + reverse('authors:login_create'))

        # Selecionar body
        body = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Not Found', body)

    def test_form_login_is_invalid(self):
        # URL inicial
        self.browser.get(self.live_server_url + reverse('authors:login_view'))

        # Selecionar formulário
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Selecionar input username
        username_field = form.find_element(By.XPATH, '//input[@placeholder="Digite seu usuário"]')

        # Selecionar input password
        password_field = form.find_element(By.XPATH, '//input[@placeholder="Digite sua senha"]')

        # Enviar caracteres para o campo username
        username_field.send_keys(' ')

        # Enviar caracteres para o campo password
        password_field.send_keys(' ')

        # Clicar no botão que contém o type submit
        form.submit()

        # A página mudou quando clicou em "form.submit()", pegar formulário novamente
        form = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Erro ao enviar o formulário', form)

    def test_login_form_invalid_credentials(self):
        # URL inicial
        self.browser.get(self.live_server_url + reverse('authors:login_view'))

        # Selecionar formulário
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Selecionar input username
        username_field = form.find_element(By.XPATH, '//input[@placeholder="Digite seu usuário"]')

        # Selecionar input password
        password_field = form.find_element(By.XPATH, '//input[@placeholder="Digite sua senha"]')

        # Enviar caracteres para o campo username
        username_field.send_keys('UsuárioNãoExiste')

        # Enviar caracteres para o campo password
        password_field.send_keys('SenhaNãoExiste')

        # A página mudou quando clicou em "form.submit()", pegar formulário novamente
        form.submit()

        form = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Usuário não existe ou a senha está incorreta, verifique suas credenciais',
                      form)
