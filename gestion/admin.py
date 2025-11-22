# gestion/admin.py
from django.contrib import admin
from django.utils.html import format_html
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
# INLINES (Para gestionar las relaciones dentro del Proyecto)
# ----------------------------------------

class MuroInline(admin.TabularInline):
    """Permite editar los Muros de un Proyecto directamente en el formulario de Proyecto."""
    model = Muro
    extra = 1
    fields = ('ubicacion', 'superficie', 'material_aislante')
    autocomplete_fields = ['material_aislante']


class ResultadoCEVInline(admin.StackedInline):
    """Permite ver/crear el Resultado CEV (1:1) de un Proyecto."""
    model = ResultadoCEV
    max_num = 1
    can_delete = False
    verbose_name_plural = 'Resultado de Calificación Energética'
    fields = ('calificacion', 'consumo_energia_anual', 'fecha_calificacion')


# ----------------------------------------
# ADMIN: PROYECTO (Principal)
# ----------------------------------------

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cliente', 'tipo', 'fecha_inicio', 'estado_badge', 'calificacion_estimada')
    list_filter = ('tipo', 'fecha_inicio', 'cliente')
    search_fields = ('nombre', 'cliente__nombre', 'descripcion')
    date_hierarchy = 'fecha_inicio'
    filter_horizontal = ('sistemas',)
    
    # Inlines
    inlines = [MuroInline, ResultadoCEVInline]
    
    # Organización de campos en el formulario
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'cliente', 'tipo', 'fecha_inicio'),
        }),
        ('Sistemas Instalados (Relación N:M)', {
            'fields': ('sistemas',),
            'classes': ('collapse',),
        }),
    )
    
    # Autocomplete para mejorar la búsqueda
    autocomplete_fields = ['cliente']
    
    def estado_badge(self, obj):
        """Muestra un badge colorido del estado."""
        estado = obj.get_estado_display()
        badge_class = obj.get_badge_class()
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            badge_class,
            estado
        )
    estado_badge.short_description = 'Estado'
    
    def calificacion_estimada(self, obj):
        """Muestra la calificación energética estimada."""
        calificacion = obj.calcular_calificacion_energetica()
        badge_class = obj.get_badge_class()
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            badge_class,
            calificacion
        )
    calificacion_estimada.short_description = 'Calificación Estimada'


# ----------------------------------------
# ADMIN: CLIENTE
# ----------------------------------------

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto', 'total_proyectos_display')
    search_fields = ('nombre', 'contacto')
    ordering = ('nombre',)
    
    def total_proyectos_display(self, obj):
        """Muestra el total de proyectos del cliente."""
        total = obj.total_proyectos()
        return format_html(
            '<span style="font-weight: bold; color: #007bff;">{}</span>',
            total
        )
    total_proyectos_display.short_description = 'Total Proyectos'


# ----------------------------------------
# ADMIN: TIPO PROYECTO
# ----------------------------------------

@admin.register(TipoProyecto)
class TipoProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'total_proyectos')
    search_fields = ('nombre',)
    
    def total_proyectos(self, obj):
        """Cuenta cuántos proyectos tienen este tipo."""
        return obj.proyecto_set.count()
    total_proyectos.short_description = 'Proyectos con este tipo'


# ----------------------------------------
# ADMIN: MATERIAL
# ----------------------------------------

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'conductividad', 'total_muros')
    list_filter = ('conductividad',)
    search_fields = ('nombre',)
    ordering = ('conductividad',)
    
    def total_muros(self, obj):
        """Muestra cuántos muros usan este material."""
        return obj.muros.count()
    total_muros.short_description = 'Muros que lo usan'


# ----------------------------------------
# ADMIN: SISTEMA CLIMATIZACIÓN
# ----------------------------------------

@admin.register(SistemaClimatizacion)
class SistemaClimatizacionAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'eficiencia_nominal', 'total_proyectos')
    list_filter = ('eficiencia_nominal',)
    search_fields = ('tipo',)
    
    def total_proyectos(self, obj):
        """Cuenta en cuántos proyectos está este sistema."""
        return obj.proyectos.count()
    total_proyectos.short_description = 'Proyectos que lo usan'


# ----------------------------------------
# ADMIN: RESULTADO CEV
# ----------------------------------------

@admin.register(ResultadoCEV)
class ResultadoCEVAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'calificacion_badge', 'consumo_energia_anual', 'fecha_calificacion')
    list_filter = ('calificacion', 'fecha_calificacion')
    search_fields = ('proyecto__nombre',)
    date_hierarchy = 'fecha_calificacion'
    
    def calificacion_badge(self, obj):
        """Muestra la calificación con un badge colorido."""
        badge_class = obj.get_badge_class()
        return format_html(
            '<span class="badge badge-{}" style="font-size: 14px; padding: 5px 10px;">{}</span>',
            badge_class,
            obj.get_calificacion_display()
        )
    calificacion_badge.short_description = 'Calificación'


# ----------------------------------------
# ADMIN: MURO (Opcional - si quieres gestionarlos independientemente)
# ----------------------------------------

@admin.register(Muro)
class MuroAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'ubicacion', 'superficie', 'material_aislante')
    list_filter = ('material_aislante', 'ubicacion')
    search_fields = ('proyecto__nombre', 'ubicacion')
    autocomplete_fields = ['proyecto', 'material_aislante']


# ----------------------------------------
# PERSONALIZACIÓN DEL ADMIN
# ----------------------------------------

admin.site.site_header = "Administración SAAS CEV"
admin.site.site_title = "SAAS CEV Admin"
admin.site.index_title = "Panel de Control - Calificación Energética de Viviendas"



