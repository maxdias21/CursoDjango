from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime
from tag.models import Tag
from collections import defaultdict
from django.core.validators import ValidationError
# Tradução
# Recomendado o lazy para models
from django.utils.translation import gettext_lazy


# from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.

class NewsManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True)


class News(models.Model):
    # Permite criar um ‘manager’ para criar várias funções úteis
    # No caso, eu sempre recebo as receitas com is_published=True, criei uma função para fazer isso lá no NewsManager
    objects = NewsManager()

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False,
                               verbose_name=gettext_lazy('Author'))
    title = models.CharField(max_length=255, verbose_name=gettext_lazy('Title'))
    description = models.TextField(verbose_name=gettext_lazy('Description'))
    content = models.TextField(verbose_name=gettext_lazy('Content'))
    image = models.ImageField(upload_to='news/covers/%Y/%m/%d', null=False, blank=False,
                              verbose_name=gettext_lazy('Image'))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_published = models.BooleanField(default=False, verbose_name=gettext_lazy('Published'))
    slug = models.SlugField(unique=True, blank=False, null=False, max_length=255)
    type = models.CharField(choices=(
        ('News', 'Notícias'),
        ('MainNews', 'Notícias principais'),
        ('SecondaryNewsTop', 'Notícias secundárias topo'),
        ('SecondaryNewsBottom', 'Notícias secundárias baixo'),

    ), max_length=26, blank=True, default='News', verbose_name=gettext_lazy('Type'))
    qty_read = models.IntegerField(default=0)

    # Relação gerérica com o model Tag
    # Não estou usando ContentType, estou testando ManyToManyField
    # Mais obs nos models de tag
    # tags = GenericRelation(Tag, related_query_name='News')
    tags = models.ManyToManyField(Tag)

    # Isso valida qualquer formulário, não só aqui
    def clean(self):
        error_messages = defaultdict(list)

        # Validando se já existe uma notícia com esse título
        news_from_db = News.objects.filter(title__iexact=self.title).first()

        if news_from_db:
            if news_from_db.pk != self.pk:
                error_messages['title'].append('Já existe um título com essa matéria, coloque um título diferente')

        if error_messages:
            raise ValidationError(error_messages)

        time = datetime.now()
        time_slug = time.strftime('%d %m %Y %I %M %S')
        self.slug = slugify(f'{self.title}-{time_slug}')

    class Meta:
        verbose_name_plural = gettext_lazy('News')
        verbose_name = gettext_lazy('News')

    def __str__(self):
        return self.title
