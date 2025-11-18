from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('singup/', views.SingUpView.as_view(), name='singup'),
    path('accounts/login/', views.RequestLogin.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/profile/', views.profile_view, name='profile'),
]

