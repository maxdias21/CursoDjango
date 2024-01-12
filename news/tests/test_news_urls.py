from django.test import TestCase
from django.urls import reverse


class NewsUrlsTest(TestCase):
    def test_url_news_is_correct(self):
        # Http response | status code e várias outras coisas...
        news_url = reverse('news:news', )

        self.assertEqual(news_url, '/')
