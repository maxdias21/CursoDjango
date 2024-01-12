from news.tests.test_news_base import NewsTestBase
from django.urls import resolve
from news import views


class TestViewTest(NewsTestBase):
    def test_news_view_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve('/')

        # Com function view
        #self.assertIs(views.news, view.func)

        # Com classe base view
        self.assertIs(views.NewsView, view.func.view_class)

    def test_news_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve('/')

        self.assertIs(view.app_name, 'news')

    def test_recipe_view_return_status_code_200_ok(self):
        # Http response | status code e várias outras coisas...
        response = self.client.get('/')

        self.assertIs(response.status_code, 200)
