# gestion/views.py

from django.views.generic import (
    TemplateView, # 👈 Nueva importación para la Home View
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.urls import reverse_lazy
from .models import Proyecto, Cliente, Muro 
from datetime import date 


# --- VISTA HOME (Ruta Raíz /) ---
class HomeView(TemplateView):
    """Vista simple para la página de inicio."""
    template_name = 'gestion/home.html'


# --- VISTAS CRUD PARA PROYECTOS (VIVIENDAS CEV) ---

# R - READ (Listar todos los proyectos) - Incluye Requisito 5 (Consulta ORM)
class ProyectoListView(ListView):
    """Muestra una lista de todos los Proyectos (Viviendas)."""
    model = Proyecto
    template_name = 'gestion/proyecto_list.html'
    context_object_name = 'proyectos' 
    
    # REQUISITO 5: DEMOSTRACIÓN DE CONSULTA ORM
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Consulta ORM: Proyectos cuya fecha de inicio es igual o posterior al inicio del mes
        today = date.today()
        first_day_of_month = today.replace(day=1)

        proyectos_recientes = Proyecto.objects.filter(
            fecha_inicio__gte=first_day_of_month
        ).order_by('-fecha_inicio')
        
        context['proyectos_recientes'] = proyectos_recientes
        
        return context

# R - READ (Ver detalles de un proyecto específico)
class ProyectoDetailView(DetailView): 
    """Muestra el detalle de un solo Proyecto."""
    model = Proyecto
    template_name = 'gestion/proyecto_detail.html'

# C - CREATE (Crear un nuevo proyecto)
class ProyectoCreateView(CreateView):
    """Permite crear un nuevo Proyecto (Vivienda)."""
    model = Proyecto
    template_name = 'gestion/proyecto_form.html'
    # Campos que el usuario podrá llenar. 
    fields = ['cliente', 'tipo', 'nombre', 'descripcion', 'fecha_inicio', 'sistemas'] 
    success_url = reverse_lazy('proyecto-list') 

# U - UPDATE (Actualizar un proyecto existente)
class ProyectoUpdateView(UpdateView):
    """Permite actualizar un Proyecto existente."""
    model = Proyecto
    template_name = 'gestion/proyecto_form.html'
    fields = ['cliente', 'tipo', 'nombre', 'descripcion', 'fecha_inicio', 'sistemas']
    
# D - DELETE (Eliminar un proyecto)
class ProyectoDeleteView(DeleteView):
    """Permite eliminar un Proyecto."""
    model = Proyecto
    template_name = 'gestion/proyecto_confirm_delete.html'
    context_object_name = 'proyecto'
    success_url = reverse_lazy('proyecto-list')