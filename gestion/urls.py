# gestion/urls.py

from django.urls import path
from .views import (
    HomeView,
    ProyectoListView, 
    ProyectoDetailView, 
    ProyectoCreateView, 
    ProyectoUpdateView, 
    ProyectoDeleteView,
    ProyectoReportePDFView,  
)

urlpatterns = [
    # 1. HOME (Dashboard con estadísticas)
    path('', HomeView.as_view(), name='home'), 
    
    # 2. CRUD: LISTADO (con filtros)
    path('proyectos/', ProyectoListView.as_view(), name='proyecto-list'),
    
    # 3. CREACIÓN
    path('proyectos/crear/', ProyectoCreateView.as_view(), name='proyecto-crear'),
    
    # 4. DETALLE (con cálculos energéticos)
    path('proyectos/<int:pk>/', ProyectoDetailView.as_view(), name='proyecto-detalle'),
    
    # 5. EDICIÓN
    path('proyectos/<int:pk>/editar/', ProyectoUpdateView.as_view(), name='proyecto-editar'),
    
    # 6. ELIMINACIÓN
    path('proyectos/<int:pk>/eliminar/', ProyectoDeleteView.as_view(), name='proyecto-eliminar'),
    
    # 7. GENERAR PDF 📄 (NUEVA FUNCIONALIDAD)
    path('proyectos/<int:pk>/pdf/', ProyectoReportePDFView.as_view(), name='proyecto-pdf'),
]