from django.shortcuts import render
from django.http import Http404
from news.models import News
# Usado apenas no try para pegar o erro correto
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Value, F
# Importei pra contar todas as notícias do site
from django.db.models.aggregates import Count
from django.db.models.functions import Concat


def test_commands_bd(request):
    if not request.user.is_authenticated or request.user.username != 'maxdias':
        raise Http404()

    """-----------------------------------------------------------------------"""
    news = News.objects.all()
    """-----------------------------------------------------------------------"""
    # Filtrar consultas
    # Retorna um query set
    filter_ = news.filter(is_published=True)
    """-----------------------------------------------------------------------"""
    # Usar order_by para organizar as minhas consultas
    # Vou usar -id para filtrar na ordem descrescente
    # Retorna um queryset
    filter_with_order_by = News.objects.all().order_by('-id')
    """-----------------------------------------------------------------------"""
    # QuerySets só são executadas quando são chamadas, ou seja, no código abaixo vou buscar todos os
    # objetos da minha news, porém não vou usar e logo fica em espera, não consome nada nas queries sql
    news_not_called = News.objects.all()
    """-----------------------------------------------------------------------"""
    # Pegar a primeira notícia com first()
    # Não retorna uma queryset
    first_news = News.objects.filter(author__username='maxdias').first()
    """-----------------------------------------------------------------------"""
    # Pegar a última notícia com last()
    # Não retorna uma queryset
    last_news = News.objects.filter(author__username='maxdias', is_published=True).last()
    """-----------------------------------------------------------------------"""
    # Pegar notícia usando get
    # Se ele não encontra, ele retorna um erro, interessante usar com try
    # Informação interessante na importação de módulos *from*
    # Não retorna uma queryset
    try:
        news_not_exists = News.objects.get(id=0)
    except ObjectDoesNotExist as ob:
        news_not_exists = ob
    """-----------------------------------------------------------------------"""
    # Fazer buscas na bd usando "ou" ao invés de "e", para isso usamos o "Q"
    news_using_q = News.objects.filter(
        Q(
            Q(type='News') |
            Q(author__username='maxdias')
        ),
        is_published=True)[0:2]
    """-----------------------------------------------------------------------"""
    # Fazer buscar com "F"
    # https://simpleisbetterthancomplex.com/tips/2016/08/23/django-tip-13-f-expressions.html
    """-----------------------------------------------------------------------"""
    # Usar Values para especificar os campos que eu desejo obter, se eu quiser mostrar apenas o
    # título + autor + data de envio do post eu posso usar o comando value para fazer o django
    # buscar apenas esses 3 campos, otimiza bastante a busca na bd
    # Retorna um dicionário
    news_using_values = News.objects.filter(is_published=True).values('author', 'title', 'created_at')[:2]
    """-----------------------------------------------------------------------"""
    # Usando LIMIT
    # Usamos fatiamento, exemplo logo acima
    """-----------------------------------------------------------------------"""
    # Usamos only para especificar quais valores vamos querer
    # Muito parecido com values, porém tem algumas diferenças
    # Se no only eu quero apenas author/title/created_at eu limito a busca, porém posso usar os outros
    # campos, deixando muito lento a busca
    # Retorna uma queryset | values() retorna dicionário
    news_using_only = News.objects.filter(is_published=True).only('author', 'title', 'created_at')
    # Posso usar no meu template os campos is_published ou qualquer outro (menos os 3 dentro do only)
    # para deixar minha busca lenta e eu ver a "merda" acontecer
    """-----------------------------------------------------------------------"""
    # Usamos defer para especificar quais valores vamos querer ocultar, é basicamente o only ao contrário
    # Retorna uma queryset
    # Todos os comentários feitos para only servem para defer
    news_using_defer = News.objects.filter(is_published=True).defer('author', 'title', 'created_at')
    """-----------------------------------------------------------------------"""
    # Count serve para contar
    # Vou contar quantas "news" eu tenho, porém vou filtrar pra de 2 maneiras
    # 1 pra buscar tudo e a 2 só para posts is_published = True
    count_news = News.objects.aggregate(Count('id'))
    count_news_published = News.objects.filter(is_published=True).aggregate(Count('id'))
    """-----------------------------------------------------------------------"""
    # Maior que
    # Retorna uma queryset
    gt_news = News.objects.filter(is_published=True, id__gt=4)
    """-----------------------------------------------------------------------"""
    # Maior ou igual a
    # Retorna uma queryset
    gte_news = News.objects.filter(is_published=True, id__gte=4)
    """-----------------------------------------------------------------------"""
    # Annotate cria uma anotação, porém não salva nada no banco de dados original
    # F serve para eu fazer referência dos objetos diretamente do bd
    # Value = Não dá para colocar espaços entre os campos, ele serve justamente para isso, mas também serve para criar
    # uma "string" e jogar qualquer valor que eu quiser
    news_full_name_person = News.objects.all().annotate(
        author__full_name=Concat(F('author__first_name'), Value(' '), F('author__last_name'))
    )
    """-----------------------------------------------------------------------"""
    # Comentário sobre isso no models de News
    news_model_manager = News.objects.get_published()

    """
        Tem muitos, mais muitos outros exemplos, na documentação tem tudo bem explicado, nada de difícil,
        caso eu volte aqui, posso ficar tranquilo pois é fácil de usar
    """

    """
        Posso usar order_by com vários campos order_by('id','title')
        Documentação: https://docs.djangoproject.com/pt-br/4.2/ref/models/querysets/#field-lookups
    """

    return render(request, 'authors/partials/commands.html', context={
        'filter': filter_,
        'filter_with_order_by': filter_with_order_by,
        'news_not_called': news_not_called,
        'first_news': first_news,
        'last_news': last_news,
        'news_not_exists': news_not_exists,
        'news_using_q': news_using_q,
        'news_using_values': news_using_values,
        'news_using_only': news_using_only,
        'news_using_defer': news_using_defer,
        'count_news': count_news['id__count'],
        'count_news_published': count_news_published['id__count'],
        'gt_news': gt_news,
        'gte_news': gte_news,
        'news_full_name_person': news_full_name_person,
        'news_model_manager': news_model_manager
    })
