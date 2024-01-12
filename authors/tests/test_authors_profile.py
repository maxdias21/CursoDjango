from django.test import TestCase
from authors.forms.profile import CreateProfile
from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthorsProfileTest(TestCase):
    def test_field_placeholder_is_correct(self):
        # Pegar formulario para testar os placeholders
        form = CreateProfile()

        # Placeholder dos campos
        fields = {
            'marital_status': '',
            'age': 'Digite sua idade',
            'hometown': 'Em qual cidade você nasceu?',
            'current_city': 'Em qual cidade você mora atualmente?',
            'phone_number': 'Seu número de telefone',
            'description': 'Um pouco sobre você... (máximo 500 caracteres)'
        }

        for key in fields.items():
            with self.subTest(key):
                placeholder = form[key[0]].field.widget.attrs['placeholder']
                self.assertEqual(key[1], placeholder)

    def test_field_help_text_is_correct(self):
        # Pegar formulario para testar os placeholders
        form = CreateProfile()

        # Help text dos campos
        fields = {
            'age': '',
            'hometown': '',
            'current_city': '',
            'phone_number': '',
            'description': ''
        }

        for key in fields.items():
            with self.subTest(key):
                help_text = form[key[0]].field.help_text
                self.assertEqual(key[1], help_text)

    def test_field_label_is_correct(self):
        # Pegar formulario para testar os placeholders
        form = CreateProfile()

        # Label dos campos
        fields = {
            'age': 'Idade',
            'hometown': 'Cidade natal',
            'current_city': 'Onde você mora atualmente?',
            'marital_status': 'Estado civil',
            'phone_number': 'Telefone',
            'description': 'Descrição',
            'profile_status': 'Privacidade do perfil'
        }

        for key in fields.items():
            with self.subTest(key):
                label = form[key[0]].label
                self.assertEqual(key[1], label)


class AuthorProfileFormIntegrationTest(DjangoTestCase):
    def setUp(self):
        password = 'Teste123'
        self._user = User.objects.create_user(first_name='First',
                                              last_name='Last',
                                              email='firstteste@gmail.com',
                                              username='Teste',
                                              password=password
                                              )

        # Logar usuário para usar o perfil
        self.client.login(username=self._user.username, password=password)

        # Preencher os campos para usar em alguns testes
        # Nenhum dado está registrado no bd
        self.form_data = {
            'age': '20',
            'hometown': 'Hometown',
            'current_city': 'Current_city',
            'marital_status': 'Solteiro',
            'phone_number': '11111111111',
            'description': 'My description',
            'photo': 'MyPhoto',
            'profile_status': 'Privado'
        }

        return super().setUp()

    def test_field_cannot_be_empty(self):
        # Sobrescrever self.form_data e colocar todos os campos vazios
        self.form_data['age'] = ''
        self.form_data['hometown'] = ''
        self.form_data['marital_status'] = ''
        self.form_data['phone_number'] = ''
        self.form_data['description'] = ''
        self.form_data['profile_status'] = ''
        self.form_data['current_city'] = ''

        # Pegar os erros de campos vazios
        self._form_data = {
            'phone_number': 'Campo telefone é obrigatório',
            'age': 'Campo idade é obrigatório',
            'hometown': 'Digite a cidade onde você nasceu',
            'description': 'Campo descrição é obrigatório',
            'current_city': 'Digite onde você mora atualmente',
            'marital_status': 'Campo estado civil é obrigatório',
            'profile_status': 'Campo status é obrigatório'
        }

        # Pegar a url
        url = reverse('authors:create_profile_create')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        for key in self._form_data.items():
            with self.subTest(key[0]):
                self.assertIn(key[1], content)

    def test_max_length_all_fields(self):
        # Modificar phone number
        self.form_data['phone_number'] = '1' * 12
        self.form_data['current_city'] = '1' * 51
        self.form_data['hometown_field'] = '1' * 51
        self.form_data['description'] = '1' * 501
        self.form_data['marital_status'] = '1' * 11
        self.form_data['profile_status'] = '1' * 8

        self._form_data = {
            'phone_number': 'Máximo de caracteres permitidos é 11',
            'current_city': 'Máximo de caracteres permitidos é 50',
            'hometown_field': 'Máximo de caracteres permitidos é 50',
            'description': 'Máximo de caracteres permitidos é 500',
            'marital_status': 'Máximo de caracteres permitidos é 10',
            'profile_status': 'Máximo de caracteres permitidos é 7',
        }

        # Pegar url
        url = reverse('authors:create_profile_create')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        for key in self._form_data.items():
            with self.subTest(key[0]):
                self.assertIn(key[1], content)

    def test_min_length_all_fields(self):
        # Modificar phone number
        self.form_data['phone_number'] = '1' * 9
        self.form_data['current_city'] = '1' * 2
        self.form_data['hometown_field'] = '1' * 2
        self.form_data['description'] = '1' * 9
        self.form_data['marital_status'] = ''
        self.form_data['profile_status'] = ''

        self._form_data = {
            'phone_number': 'Mínimo de caracteres permitidos é 11',
            'current_city': 'Mínimo de caracteres permitidos é 3',
            'hometown_field': 'Mínimo de caracteres permitidos é 3',
            'description': 'Mínimo de caracteres permitidos é 10',
            'marital_status': 'Mínimo de caracteres permitidos é 1',
            'profile_status': 'Mínimo de caracteres permitidos é 1',
        }

        # Pegar url
        url = reverse('authors:create_profile_create')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        for key in self._form_data.items():
            with self.subTest(key[0]):
                self.assertIn(key[1], content)


    def test_profile_was_save_successfuly(self):
        # Pegar url
        url = reverse('authors:create_profile_create')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn('Perfil alterado com sucesso!', content)

