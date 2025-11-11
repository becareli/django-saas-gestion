# CEVProject/urls.py (Principal)

from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    # Conecta la app 'gestion' a la ruta raíz (o a 'proyectos/' si prefieres)
    path('', include('gestion.urls')), 
]