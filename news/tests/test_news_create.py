from django.urls import reverse
from news.models import News
from .test_news_base import NewsTestBase
from authors.tests.test_authors_base import AuthorMixin


class NewsTestCreate(NewsTestBase):
    def test_news_template_loads_news(self):
        # Criar uma notícia
        news = self.make_news()

        # Http response | status code e várias outras coisas...
        response = self.client.get(reverse('news:news'))

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Testar se a descrição da notícia está publicado
        self.assertIn(news.description, content)

    def test_news_template_loads_main_news(self):
        # Criar uma notícia principal
        news = self.make_news(type='MainNews')

        # Http response | status code e várias outras coisas...
        response = self.client.get(reverse('news:news'))

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Testar se a descrição da notícia está publicado
        self.assertIn(news.description, content)

    def test_news_template_loads_secondary_top_news(self):
        # Criar uma notícia secundária topo
        news = self.make_news(type='SecondaryNewsTop')

        # Http response | status code e várias outras coisas...
        response = self.client.get(reverse('news:news'))

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Testar se a descrição da notícia está publicado
        self.assertIn(news.description, content)

    def test_news_template_loads_secondary_bottom_news(self):
        # Criar uma notícia secundário fundo
        news = self.make_news(type='SecondaryNewsBottom')

        # Http response | status code e várias outras coisas...
        response = self.client.get(reverse('news:news'))

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Testar se a descrição da notícia está publicado
        self.assertIn(news.description, content)

    def test_news_template_shows_no_news_found_if_no_news(self):
        # Deletar todas as notícias
        News.objects.all().delete()

        # Http response | status code e várias outras coisas...
        response = self.client.get(reverse('news:news'))

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn('Não há nada aqui no momento :(', content)

    def test_news_template_dont_loads_news_not_published(self):
        # Criar notícia com is_published = False
        news = self.make_news(is_published=False)

        # Http response | status code e várias outras coisas...
        response = self.client.get(reverse('news:news'))

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertNotIn(news.title, content)

    def test_new_user_first_name_and_last_name_show_template(self):
        # Criar um usuário
        user = self.make_author()

        # Criar perfil do usuário
        profile = AuthorMixin()
        profile_created = profile.create_author(username=user)

        # Http response | status code e várias outras coisas...
        response = self.client.get(reverse('news:news'))

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn(f'{profile_created.username.first_name} {profile_created.username.last_name}', content)

    def test_new_user_can_not_show_if_in_template_if_it_not_have_a_profile(self):
        # Criar um usuário
        user = self.make_author()

        # Criar perfil do usuário
        profile = AuthorMixin()
        profile_created = profile.create_author(username=user, is_active=False)

        # Http response | status code e várias outras coisas...
        response = self.client.get(reverse('news:news'))

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertNotIn(f'{profile_created.username.first_name} {profile_created.username.last_name}', content)
