from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('singup/', views.SingUpView.as_view(), name='singup'),
    path('accounts/login/', views.RequestLogin.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('create/', views.RequestCreateView.as_view(), name='request-create'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.RequestDelete.as_view(), name='request-delete'),
    re_path(r'^(?P<pk>\d+)/status/update/$', views.RequestStatusUpdate.as_view(), name='request-update'),
    path('admin/', views.AdminView.as_view(), name='admin')
]

