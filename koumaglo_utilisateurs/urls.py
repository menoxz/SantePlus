from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from axes.utils import reset

app_name = 'koumaglo_utilisateurs'
 
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profil/', views.profil, name='profil'),
    path('tentatives-connexion/', views.view_login_attempts, name='login_attempts'),
    path('deverrouiller/<str:username>/', views.unlock_account, name='unlock_account'),
] 