from django.test import TestCase
from news.models import News
from django.contrib.auth.models import User
from django.utils.text import slugify


class RecipeMixin():
    def make_author(self, first_name='First', last_name='Last', email='test_user@gmail.com', username='UsernameTest',
                    password='Password123'):
        return User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,
                                        password=password)

    def make_news(self, author=None, title='News Title', description='News Description', content='Test Content',
                  is_published=True, image='I dont have an image', type='News', slug='SlugNews'):
        if author is None:
            author = self.make_author()

        return News.objects.create(
            author=author, title=title, description=description, content=content, is_published=is_published,
            image=image, type=type, slug=slug
        )


class NewsTestBase(TestCase, RecipeMixin):
    def setUp(self):
        return super().setUp()
