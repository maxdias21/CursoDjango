from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Página inicial
    path('', views.NewsView.as_view(), name='news'),
    # Notícia completa
    path('news/<slug:slug>/', views.ReadNews.as_view(), name='created_news'),
    # Todas as notícias
    path('news/all', views.AllNews.as_view(), name='all_news'),
    # Pesquisar notícias
    path('search/', views.SearchNews.as_view(), name='search'),
    # Tags
    path('tags/<slug:slug>/', views.ViewTag.as_view(), name='tag'),
]
