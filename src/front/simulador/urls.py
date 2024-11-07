# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_principal, name='menu_principal'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('menu_usuario/<str:nombre_usuario>/', views.menu_usuario, name='menu_usuario'),
    path('simulador/', views.simular, name='simulador'),
]
