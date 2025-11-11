# gestion/urls.py

from django.urls import path
from .views import (
    HomeView, # 👈 Importación de la nueva vista Home
    ProyectoListView, 
    ProyectoDetailView, 
    ProyectoCreateView, 
    ProyectoUpdateView, 
    ProyectoDeleteView
)

urlpatterns = [
    # 1. HOME (Página Principal)
    path('', HomeView.as_view(), name='home'), 
    
    # 2. CRUD: LISTADO (READ - Ruta ahora es 'proyectos/')
    path('proyectos/', ProyectoListView.as_view(), name='proyecto-list'),
    
    # 3. CREACIÓN (CREATE)
    path('proyectos/crear/', ProyectoCreateView.as_view(), name='proyecto-crear'),
    
    # Rutas que dependen del ID (Primary Key: <int:pk>) del proyecto
    
    # 4. DETALLE (READ)
    path('proyectos/<int:pk>/', ProyectoDetailView.as_view(), name='proyecto-detalle'),
    
    # 5. EDICIÓN (UPDATE)
    path('proyectos/<int:pk>/editar/', ProyectoUpdateView.as_view(), name='proyecto-editar'),
    
    # 6. ELIMINACIÓN (DELETE)
    path('proyectos/<int:pk>/eliminar/', ProyectoDeleteView.as_view(), name='proyecto-eliminar'),
]