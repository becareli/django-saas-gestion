# gestion/models.py
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from datetime import date

# ----------------------------------------
# 1. ENTIDADES NO RELACIONADAS
# ----------------------------------------

class Material(models.Model):
    nombre = models.CharField(max_length=100)
    conductividad = models.DecimalField(max_digits=5, decimal_places=3, verbose_name="Conductividad Térmica (W/mK)")
    
    class Meta:
        verbose_name_plural = "Materiales"
    
    def __str__(self):
        return f"{self.nombre} ({self.conductividad} W/mK)"


class TipoProyecto(models.Model):
    nombre = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = "Tipos de Proyecto"
    
    def __str__(self):
        return self.nombre


# ----------------------------------------
# 2. ENTIDAD BASE CON RELACIÓN
# ----------------------------------------

class Cliente(models.Model):
    """Entidad para representar al cliente/propietario de la vivienda."""
    nombre = models.CharField(max_length=100, verbose_name="Nombre/Razón Social")
    contacto = models.CharField(max_length=100, verbose_name="Email de Contacto", unique=True)
    
    def __str__(self):
        return self.nombre
    
    def total_proyectos(self):
        """Retorna el total de proyectos del cliente."""
        return self.proyectos.count()


# ----------------------------------------
# 3. ENTIDAD RELACIONADA N:M
# ----------------------------------------

class SistemaClimatizacion(models.Model):
    """Sistemas de climatización que puede tener el proyecto."""
    tipo = models.CharField(max_length=100, verbose_name="Tipo de Sistema")
    eficiencia_nominal = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, verbose_name="Eficiencia Nominal (COP/SCOP)")
    
    class Meta:
        verbose_name_plural = "Sistemas de Climatización"
    
    def __str__(self):
        return f"{self.tipo} (Eficiencia: {self.eficiencia_nominal})"


# ----------------------------------------
# 4. ENTIDAD PRINCIPAL: PROYECTO
# ----------------------------------------

class Proyecto(models.Model):
    """Modelo principal que representa la Vivienda o el Proyecto de Calificación Energética."""
    
    # Relaciones
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='proyectos')
    tipo = models.ForeignKey(TipoProyecto, on_delete=models.PROTECT)
    sistemas = models.ManyToManyField(SistemaClimatizacion, related_name='proyectos', blank=True)

    # Campos de datos
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la Vivienda/Proyecto")
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField(default=date.today)

    class Meta:
        verbose_name_plural = "Proyectos"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"

    def get_estado_display(self):
        """Retorna el estado del proyecto basado en si tiene calificación."""
        try:
            resultado = self.resultados
            return f"Calificado ({resultado.calificacion})"
        except ObjectDoesNotExist:
            return "En Curso"
    
    # ----------------------------------------
    # MÉTODOS DE CÁLCULO ENERGÉTICO
    # ----------------------------------------
    
    def calcular_calificacion_energetica(self):
        """
        Calcula la calificación energética basada en:
        - Materiales aislantes
        - Superficie de muros
        - Conductividad térmica
        """
        total_conductividad = 0
        total_superficie = 0
        
        for muro in self.muros.all():
            total_conductividad += (
                float(muro.material_aislante.conductividad) * 
                float(muro.superficie)
            )
            total_superficie += float(muro.superficie)
        
        if total_superficie > 0:
            promedio_conductividad = total_conductividad / total_superficie
            
            # Criterios de calificación energética
            if promedio_conductividad < 0.5:
                return 'A+'
            elif promedio_conductividad < 1.0:
                return 'A'
            elif promedio_conductividad < 1.5:
                return 'B'
            elif promedio_conductividad < 2.0:
                return 'C'
            else:
                return 'D'
        
        return 'Sin datos'
    
    def calcular_consumo_estimado(self):
        """Estima el consumo energético anual en kWh/m²."""
        calificacion = self.calcular_calificacion_energetica()
        
        consumos = {
            'A+': 50,
            'A': 75,
            'B': 100,
            'C': 150,
            'D': 200,
            'Sin datos': 0
        }
        
        return consumos.get(calificacion, 0)
    
    def get_badge_class(self):
        """Retorna la clase CSS para el badge según la calificación."""
        try:
            calificacion = self.resultados.calificacion
        except ObjectDoesNotExist:
            calificacion = self.calcular_calificacion_energetica()
        
        badges = {
            'A+': 'success',
            'A': 'primary',
            'B': 'info',
            'C': 'warning',
            'D': 'danger',
            'Sin datos': 'secondary'
        }
        
        return badges.get(calificacion, 'secondary')


# ----------------------------------------
# 5. ENTIDAD RELACIONADA 1:1
# ----------------------------------------

class ResultadoCEV(models.Model):
    """Almacena la calificación final del proyecto (Relación 1:1)."""
    
    CALIFICACIONES = (
        ('A+', 'A+ (Excelente)'),
        ('A', 'A (Muy Bueno)'),
        ('B', 'B (Bueno)'),
        ('C', 'C (Estándar)'),
        ('D', 'D (Malo)'),
    )
    
    # Relación 1:1
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE, related_name='resultados')
    calificacion = models.CharField(max_length=2, choices=CALIFICACIONES)
    consumo_energia_anual = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Consumo Anual (kWh/m²)")
    fecha_calificacion = models.DateField(default=date.today)

    class Meta:
        verbose_name = "Resultado CEV"
        verbose_name_plural = "Resultados CEV"

    def __str__(self):
        return f"Resultado de {self.proyecto.nombre}: {self.calificacion}"
    
    def get_badge_class(self):
        """Retorna la clase CSS para el badge según la calificación."""
        badges = {
            'A+': 'success',
            'A': 'primary',
            'B': 'info',
            'C': 'warning',
            'D': 'danger'
        }
        return badges.get(self.calificacion, 'secondary')


# ----------------------------------------
# 6. ENTIDAD RELACIONADA 1:N
# ----------------------------------------

class Muro(models.Model):
    """Componente de la envolvente (muros, techos) asociado a un proyecto."""
    
    # Relaciones
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='muros')
    material_aislante = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='muros')

    # Campos
    ubicacion = models.CharField(max_length=50, verbose_name="Ubicación (Norte, Sur, etc.)")
    superficie = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Superficie (m²)")
    
    class Meta:
        verbose_name_plural = "Muros"
    
    def __str__(self):
        return f"Muro {self.ubicacion} del Proyecto {self.proyecto.nombre}"