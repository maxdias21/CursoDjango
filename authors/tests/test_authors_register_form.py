from authors.forms import RegisterForm
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthorRegisterFormUnitTest(TestCase):
    def test_fields_placeholder_is_correct(self):
        # Pegar formulário para testar os placeholders
        form = RegisterForm()

        # Placeholder dos campos authors | register
        fields = {
            'first_name': 'Seu nome',
            'last_name': 'Seu sobrenome',
            'username': 'Digite um nome de usuário válido',
            'email': 'Digite um email válido',
            'password': 'Crie uma senha',
            'password2': 'Repita sua senha'
        }

        for key in fields.items():
            with self.subTest(key):
                placeholder = form[key[0]].field.widget.attrs['placeholder']
                self.assertEqual(key[1], placeholder, msg=f'Field: {key[1]} is invalid')

    def test_fields_help_text_is_correct(self):
        # Pegar formulário para testar os help_text
        form = RegisterForm()

        # Help_text dos campos authors | register
        fields = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'email': '',
            'password': '',
            'password2': ''
        }

        for key in fields.items():
            with self.subTest(key):
                help_text = form[key[0]].field.help_text
                self.assertEqual(key[1], help_text, msg=f'Field {key[0]}: {key[1]} is invalid')

    def test_fields_label_is_correct(self):
        # Pegar formulário para testar as labels
        form = RegisterForm()

        # Labels dos campos authors | register
        fields = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Usuário',
            'email': 'Email',
            'password': 'Senha',
            'password2': 'Repita sua senha'
        }

        for key in fields.items():
            with self.subTest(key):
                label = form[key[0]].field.label
                self.assertEqual(key[1], label, msg=f'Field {key[0]}: {key[1]} is invalid')


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self):
        # Criar um usuário para usar em alguns testes
        User.objects.create_user(username='MyUserTest', email='email@gmail.com', password='Test123456')

        # Preencher os campos para usar em alguns testes
        # Nenhum dado está registrado no bd
        self.form_data = {
            'first_name': 'Test123',
            'last_name': '123Test',
            'username': 'MyUserTest123',
            'email': 'emailtest@gmail.com',
            'password': 'Password123',
            'password2': 'Password123',
        }
        return super().setUp()

    def test_field_cannot_be_empty(self):
        # Sobrescrever self.form_data e colocar todos os campos vazios
        self.form_data['first_name'] = ''
        self.form_data['last_name'] = ''
        self.form_data['username'] = ''
        self.form_data['email'] = ''
        self.form_data['password'] = ''
        self.form_data['password2'] = ''

        # Pegar os erros de campos vazios
        self._form_data = {
            'first_name': 'Preencha o campo nome',
            'last_name': 'Preencha o campo sobrenome',
            'username': 'Digite um usuário válido',
            'password': 'Digite uma senha',
            'password2': 'Digite uma senha',

        }

        # Pegar a url
        url = reverse('authors:register_create')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        for key in self._form_data.items():
            with self.subTest(key[0]):
                self.assertIn(key[1], content)

    def test_username_field_min_length_should_be_4(self):
        # Modificar o username
        self.form_data['username'] = 'A' * 3

        # Pegar a url
        url = reverse('authors:register_create')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Mensagem do erro
        msg = 'Usuário deve conter 4 caracteres ou mais'

        self.assertIn(msg, content)

    def test_username_field_max_length_should_be_20(self):
        # Modificar o username
        self.form_data['username'] = 'A' * 21

        # Pegar a url
        url = reverse('authors:register_create')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Mensagem do erro
        msg = 'Máximo de caracteres permitido é 20'

        self.assertIn(msg, content)

    def test_password_field_min_length_should_be_6(self):
        # Modificar o password
        self.form_data['password'] = 'A' * 5

        # Pegar a url
        url = reverse('authors:register_create')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Mensagem do erro
        msg = 'Senha deve conter 6 caracteres ou mais'

        self.assertIn(msg, content)

    def test_password_field_max_length_should_be_50(self):
        # Modificar o password
        self.form_data['password'] = 'A' * 51

        # Pegar a url
        url = reverse('authors:register_create')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Mensagem do erro
        msg = 'Máximo de caracteres permitido é 50'

        self.assertIn(msg, content)

    def test_password2_field_min_length_should_be_6(self):
        # Modificar o password2
        self.form_data['password2'] = 'A' * 5

        # Pegar a url
        url = reverse('authors:register_create')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Mensagem do erro
        msg = 'Senha deve conter 6 caracteres ou mais'

        self.assertIn(msg, content)

    def test_password2_field_max_length_should_be_50(self):
        # Modificar o password2
        self.form_data['password2'] = 'A' * 51

        # Pegar a url
        url = reverse('authors:register_create')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Mensagem do erro
        msg = 'Máximo de caracteres permitido é 50'

        self.assertIn(msg, content)

    def test_password_and_password2_confirmation_are_equal(self):
        # Modificar o password | password do form_data
        self.form_data['password'] = 'Test1234'
        self.form_data['password2'] = 'Test12345'

        # Pegar a url
        url = reverse('authors:register_create')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Mensagem do erro
        msg = 'Senhas precisam ser iguais'

        self.assertIn(msg, content)

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_is_exists(self):
        # Modificar o email do form_data | estou usando um email que eu criei no setup
        self.form_data['email'] = 'email@gmail.com'
        # Pegar a url
        url = reverse('authors:register_create')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Mensagem do erro
        msg = 'Email já cadastrado'

        self.assertIn(msg, content)

    def test_author_created_can_login(self):
        # Pegar a url
        url = reverse('authors:register_create')

        # Redireciona pra register_create | cria o usuário
        self.client.post(url, data=self.form_data, follow=True)

        # Autenticar usuário | retorna True ou False
        is_authenticated = self.client.login(username=self.form_data['username'],
                                             password=self.form_data['password'])

        # Verificar se usuário está logado
        self.assertTrue(is_authenticated)
