# gestion/views.py

from django.views.generic import (
    TemplateView,
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.urls import reverse_lazy
from django.db.models import Count, Avg
from .models import Proyecto, Cliente, Muro, ResultadoCEV
from datetime import date
from django.http import HttpResponse


# --- VISTA HOME CON DASHBOARD ---
class HomeView(TemplateView):
    """Vista mejorada con estadísticas del dashboard."""
    template_name = 'gestion/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas generales
        context['total_proyectos'] = Proyecto.objects.count()
        context['total_clientes'] = Cliente.objects.count()
        
        # Proyectos con resultados vs sin resultados
        context['proyectos_calificados'] = Proyecto.objects.filter(resultados__isnull=False).count()
        context['proyectos_en_curso'] = Proyecto.objects.filter(resultados__isnull=True).count()
        
        # Distribución de calificaciones
        context['calificaciones'] = ResultadoCEV.objects.values('calificacion').annotate(
            count=Count('id')
        ).order_by('calificacion')
        
        # Proyectos recientes (últimos 5)
        context['proyectos_recientes'] = Proyecto.objects.select_related(
            'cliente', 'tipo'
        ).order_by('-fecha_inicio')[:5]
        
        return context


# --- VISTAS CRUD PARA PROYECTOS ---

class ProyectoListView(ListView):
    """Lista de proyectos con filtros."""
    model = Proyecto
    template_name = 'gestion/proyecto_list.html'
    context_object_name = 'proyectos'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('cliente', 'tipo').prefetch_related('sistemas')
        
        # Filtro por búsqueda
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(nombre__icontains=search)
        
        # Filtro por cliente
        cliente_id = self.request.GET.get('cliente')
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        
        # Filtro por tipo
        tipo_id = self.request.GET.get('tipo')
        if tipo_id:
            queryset = queryset.filter(tipo_id=tipo_id)
        
        return queryset.order_by('-fecha_inicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Proyectos recientes del mes
        today = date.today()
        first_day_of_month = today.replace(day=1)
        context['proyectos_recientes'] = Proyecto.objects.filter(
            fecha_inicio__gte=first_day_of_month
        ).order_by('-fecha_inicio')
        
        # Para los filtros
        from .models import TipoProyecto
        context['clientes'] = Cliente.objects.all()
        context['tipos'] = TipoProyecto.objects.all()
        
        return context


class ProyectoDetailView(DetailView):
    """Detalle del proyecto con cálculos energéticos."""
    model = Proyecto
    template_name = 'gestion/proyecto_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calcular calificación energética estimada
        proyecto = self.object
        context['calificacion_estimada'] = proyecto.calcular_calificacion_energetica()
        context['consumo_estimado'] = proyecto.calcular_consumo_estimado()
        
        # Información de muros
        context['muros'] = proyecto.muros.select_related('material_aislante').all()
        
        return context


class ProyectoCreateView(CreateView):
    """Crear nuevo proyecto."""
    model = Proyecto
    template_name = 'gestion/proyecto_form.html'
    fields = ['cliente', 'tipo', 'nombre', 'descripcion', 'fecha_inicio', 'sistemas']
    success_url = reverse_lazy('proyecto-list')


class ProyectoUpdateView(UpdateView):
    """Actualizar proyecto existente."""
    model = Proyecto
    template_name = 'gestion/proyecto_form.html'
    fields = ['cliente', 'tipo', 'nombre', 'descripcion', 'fecha_inicio', 'sistemas']
    
    def get_success_url(self):
        return reverse_lazy('proyecto-detalle', kwargs={'pk': self.object.pk})


class ProyectoDeleteView(DeleteView):
    """Eliminar proyecto."""
    model = Proyecto
    template_name = 'gestion/proyecto_confirm_delete.html'
    context_object_name = 'proyecto'
    success_url = reverse_lazy('proyecto-list')


# --- VISTA PARA GENERAR PDF ---
class ProyectoReportePDFView(DetailView):
    """Genera un reporte PDF del proyecto."""
    model = Proyecto
    
    def render_to_response(self, context, **response_kwargs):
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
        except ImportError:
            return HttpResponse("Instala reportlab: pip install reportlab", status=500)
        
        proyecto = self.get_object()
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte_{proyecto.nombre}.pdf"'
        
        # Crear PDF
        p = canvas.Canvas(response, pagesize=letter)
        
        # Título
        p.setFont("Helvetica-Bold", 20)
        p.drawString(100, 750, f"Reporte CEV: {proyecto.nombre}")
        
        # Información del proyecto
        p.setFont("Helvetica", 12)
        y = 700
        p.drawString(100, y, f"Cliente: {proyecto.cliente.nombre}")
        y -= 20
        p.drawString(100, y, f"Tipo: {proyecto.tipo.nombre}")
        y -= 20
        p.drawString(100, y, f"Fecha de Inicio: {proyecto.fecha_inicio}")
        y -= 30
        
        # Calificación
        try:
            resultado = proyecto.resultados
            p.setFont("Helvetica-Bold", 16)
            p.drawString(100, y, f"Calificación: {resultado.calificacion}")
            y -= 25
            p.setFont("Helvetica", 12)
            p.drawString(100, y, f"Consumo: {resultado.consumo_energia_anual} kWh/m²")
        except:
            calificacion_est = proyecto.calcular_calificacion_energetica()
            p.setFont("Helvetica-Bold", 16)
            p.drawString(100, y, f"Calificación Estimada: {calificacion_est}")
            y -= 25
            consumo_est = proyecto.calcular_consumo_estimado()
            p.setFont("Helvetica", 12)
            p.drawString(100, y, f"Consumo Estimado: {consumo_est} kWh/m²")
        
        p.showPage()
        p.save()
        
        return response