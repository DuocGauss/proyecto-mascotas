from django.urls import path, include
from . import views





urlpatterns = [
    path("", views.index, name="index"),
    path('registro/',views.registro, name='registro'),
    path('login_custom/', views.login_custom, name='login_custom'),
    path('logout_custom/', views.logout_custom, name='logout_custom'),
    path('cuidador/', views.cuidador, name='cuidador'),
    path('perfil/', views.perfil, name='perfil'),
]