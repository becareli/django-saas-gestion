# gestion/admin.py
from django.contrib import admin
from .models import (
    Proyecto, 
    Cliente, 
    TipoProyecto, 
    SistemaClimatizacion, 
    Material, 
    Muro, 
    ResultadoCEV
)

# ----------------------------------------
# INLINES (Para gestionar las relaciones dentro del Proyecto) - REQUISITO 7
# ----------------------------------------

class MuroInline(admin.TabularInline):
    """Permite editar los Muros de un Proyecto directamente en el formulario de Proyecto."""
    model = Muro
    extra = 1

class ResultadoCEVInline(admin.StackedInline):
    """Permite ver/crear el Resultado CEV (1:1) de un Proyecto."""
    model = ResultadoCEV
    max_num = 1
    can_delete = False
    verbose_name_plural = 'Resultado de Calificación Energética'

# ----------------------------------------
# REGISTROS DE MODELOS
# ----------------------------------------

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    # Requisito 7: Listado y Búsqueda
    list_display = ('nombre', 'cliente', 'tipo', 'fecha_inicio', 'get_estado_display')
    list_filter = ('tipo', 'fecha_inicio')
    search_fields = ('nombre', 'cliente__nombre')
    date_hierarchy = 'fecha_inicio'
    
    # Inlines
    inlines = [MuroInline, ResultadoCEVInline]
    
    # Organización de campos en el formulario
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'cliente', 'tipo', 'fecha_inicio'),
        }),
        ('Sistemas Instalados (Relación N:M)', {
            'fields': ('sistemas',),
            'classes': ('collapse',), # Esto hace que se pueda colapsar/expandir
        }),
    )

# ----------------------------------------
# MODELOS BASE (CLAVE para el Pop-up)
# ----------------------------------------

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """
    El registro de Cliente es necesario para que el botón '+' aparezca
    en el formulario de Proyecto (ForeignKey).
    """
    list_display = ('nombre', 'contacto')
    search_fields = ('nombre', 'contacto')

@admin.register(TipoProyecto)
class TipoProyectoAdmin(admin.ModelAdmin):
    # El registro es igualmente clave para el pop-up de TipoProyecto
    list_display = ('nombre',)
    search_fields = ('nombre',)


# ----------------------------------------
# OTROS REGISTROS
# ----------------------------------------

admin.site.register(Material)
admin.site.register(SistemaClimatizacion)

# NOTA: Muro y ResultadoCEV ya están gestionados con Inlines, 
# por lo que no necesitan un registro de admin.site.register directo, 
# a menos que quieras acceder a ellos de forma independiente.