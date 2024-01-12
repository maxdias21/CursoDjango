from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    # Login
    path('login/', views.Login.as_view(), name='login_view'),
    path('login/create', views.Login.as_view(), name='login_create'),
    # Registrar
    path('register/', views.RegisterPerson.as_view(), name='register_view'),
    path('register/create', views.RegisterPerson.as_view(), name='register_create'),
    # Logout
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # Criar perfil + editar perfil + visualizar perfil
    path('profile/create/', views.CreatePersonProfile.as_view(), name='create_profile_view'),
    path('profile/create/create', views.CreatePersonProfile.as_view(), name='create_profile_create'),
    path('profile/create/edit', views.EditPersonProfile.as_view(), name='profile_edit'),
    path('profile/my-profile/', views.ProfilePerson.as_view(), name='profile'),
    path('profile/<slug:slug>', views.ViewSomeonePerson.as_view(), name='profile_complete_person'),
    # Pesquisar perfil
    path('profile/', views.SearchPeople.as_view(), name='profile_person'),
    # Testes
    path('tests', views.test_commands_bd, name='just_tests')

]
