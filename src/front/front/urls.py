from django.contrib import admin
from django.urls import path, include
from simulador import views  # Importa las vistas de tu aplicación simulador

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('simulador.urls')),  # Asegúrate de incluir las rutas de 'simulador'
]
