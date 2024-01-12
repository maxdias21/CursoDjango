from .base import AuthorBaseTest
from selenium.webdriver.common.by import By
from django.urls import reverse
from selenium.webdriver.common.keys import Keys
from time import sleep


class AuthorsRegisterTest(AuthorBaseTest):
    def get_form(self):
        return self.browser.find_element(By.XPATH, '/html/body/section/div/div[2]/div/form')

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 10)

    def form_field_test_with_callback(self, callback):
        # URL inicial
        self.browser.get(self.live_server_url + reverse('authors:register_view'))

        # Selecionar formulário
        form = self.get_form()

        # Preencher todos os outros campos com espaços, menos o email
        self.fill_form_dummy_data(form)

        # Selecionar campo do email
        email_field = form.find_element(By.NAME, 'email')

        # Preencher o campo email
        email_field.send_keys('teste@gmail.com')

        # Chamar função callback
        callback(form)

        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            # Selecionar campo do nome
            first_name_field = self.get_by_placeholder(form, 'Seu nome')

            # Enviar caracteres para o campo nome
            first_name_field.send_keys(' ')

            # Pressionar a tecla enter (seleciona o input caso todos os campos tenham sido preenchidos)
            # Se não, o enter passa para o próximo campo não preenchido
            first_name_field.send_keys(Keys.ENTER)

            # A página recarregou quando clicou em "form.submit()", pegar formulário novamente
            form = self.browser.find_element(By.XPATH, '/html/body/section/div/div[2]/div/form')

            self.assertIn('Preencha o campo nome', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            # Selecionar campo do sobrenome
            last_name_field = self.get_by_placeholder(form, 'Seu sobrenome')

            # Enviar caracteres para o campo sobrenome
            last_name_field.send_keys(' ')

            # Pressionar a tecla enter (seleciona o input caso todos os campos tenham sido preenchidos)
            # Se não, o enter passa para o próximo campo não preenchido
            last_name_field.send_keys(Keys.ENTER)

            # A página recarregou quando clicou em "form.submit()", pegar formulário novamente
            form = self.browser.find_element(By.XPATH, '/html/body/section/div/div[2]/div/form')

            self.assertIn('Preencha o campo sobrenome', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            # Selecionar campo do usuário
            username_field = self.browser.find_element(form, 'Digite um nome de usuário válido')

            # Enviar caracteres para o campo usuário
            username_field.send_keys(' ')

            # Pressionar a tecla enter (seleciona o input caso todos os campos tenham sido preenchidos)
            # Se não, o enter passa para o próximo campo não preenchido
            username_field.send_keys(Keys.ENTER)

            # A página recarregou quando clicou em "form.submit()", pegar formulário novamente
            form = self.browser.find_element(By.XPATH, '/html/body/section/div/div[2]/div/form')

            self.assertIn('Este campo é obrigatório.', form.text)

        self.form_field_test_with_callback(callback)

    def test_error_email_field(self):
        def callback(form):
            email_field = self.browser.find_element(By.XPATH, 'Digite um email válido')

            # Estou apagando tudo que está no campo email
            email_field.clear()

            # Enviar caracteres para o campo email sem o ponto para dar o erro
            # Estou sobrescrevendo
            email_field.send_keys('teste@gmail')

            # Pressionar a tecla enter (seleciona o input caso todos os campos tenham sido preenchidos)
            # Se não, o enter passa para o próximo campo não preenchido
            email_field.send_keys(Keys.ENTER)

            # A página recarregou quando clicou em "form.submit()", pegar formulário novamente
            form = self.browser.find_element(By.XPATH, '/html/body/section/div/div[2]/div/form')

            self.assertIn('Informe um endereço de email válido.', form.text)

        self.form_field_test_with_callback(callback)

    def test_passwords_dont_match(self):
        def callback(form):
            password_field1 = self.get_by_placeholder(form, 'Crie uma senha')
            password_field2 = self.get_by_placeholder(form, 'Repita sua senha')

            # Estou apagando tudo que está no campo senha
            password_field1.clear()

            # Estou apagando tudo que está no campo repetir senha
            password_field2.clear()

            # Enviar caracteres para o campo senha
            password_field1.send_keys('PasswordField1')

            # Enviar caracteres para o campo repetir senha
            password_field2.send_keys('PasswordField2')

            # Pressionar a tecla enter (seleciona o input caso todos os campos tenham sido preenchidos)
            # Se não, o enter passa para o próximo campo não preenchido
            password_field2.send_keys(Keys.ENTER)

            # A página recarregou quando clicou em "form.submit()", pegar formulário novamente
            form = self.browser.find_element(By.XPATH, '/html/body/section/div/div[2]/div/form')

            self.assertIn('Senhas precisam ser iguais', form.text)

        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        # URL inicial
        self.browser.get(self.live_server_url + reverse('authors:register_view'))

        # Selecionar o formulário
        form = self.browser.find_element(By.XPATH, '/html/body/section/div/div[2]/div/form')

        # Selecionar campo do nome e enviar valores
        first_name_field = self.get_by_placeholder(form, 'Seu nome')
        first_name_field.send_keys('First')

        # Selecionar campo do sobrenome e enviar valores
        last_name_field = self.get_by_placeholder(form, 'Seu sobrenome')
        last_name_field.send_keys('Name')

        # Selecionar campo do usuário e enviar valores
        username_field = self.get_by_placeholder(form, 'Digite um nome de usuário válido')
        username_field.send_keys('Test_Username')

        # Selecionar campo do email e enviar valores
        email_field = self.get_by_placeholder(form, 'Digite um email válido')
        email_field.send_keys('test_field@gmail.com')

        # Selecionar campo da senha e enviar valores
        password_field = self.get_by_placeholder(form, 'Crie uma senha')
        password_field.send_keys('PasswordTest123')

        # Selecionar campo do repita sua senha e enviar valores
        password2_field = self.get_by_placeholder(form, 'Repita sua senha')
        password2_field.send_keys('PasswordTest123')

        # Clicar no botão que contém o type submit
        form.submit()

        # A página mudou quando clicou em "form.submit()", pegar formulário novamente
        form = self.browser.find_element(By.XPATH, '/html/body/section/div/div[2]/div/form').text

        self.assertIn('Seu usuário foi registrado com sucesso!', form)
