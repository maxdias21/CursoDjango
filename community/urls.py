from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # Início + visualizar post específico
    path('', views.CommunityHome.as_view(), name='community'),
    path('<slug:slug>/', views.ViewCommunityPosts.as_view(), name='view_community_post'),
    # Criar posts
    path('post/create/', views.CreateCommunityPost.as_view(), name='create_community_post_view'),
    # Criar post
    path('post/create/create', views.CreateCommunityPost.as_view(), name='create_community_post_create'),
    # Ver meus posts + deletar
    path('post/my-posts/', views.MyPosts.as_view(), name='my_posts'),
    path('post/my_posts/delete/<int:id>', views.DeleteCommunityPost.as_view(), name='delete_post'),
    # Todos os posts + search
    path('posts/all/', views.AllPostsCommunity.as_view(), name='all_posts'),
    path('posts/search/', views.SearchCommunityPosts.as_view(), name='search_posts'),
    path('posts/all/<slug:slug>', views.AllPersonPosts.as_view(), name='all_post_person')
]
