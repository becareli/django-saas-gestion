# gestion/models.py
from django.db import models
from datetime import date

# ----------------------------------------
# 1. ENTIDADES NO RELACIONADAS (REQUISITO 2)
# ----------------------------------------

class Material(models.Model):
    nombre = models.CharField(max_length=100)
    conductividad = models.DecimalField(max_digits=5, decimal_places=3, verbose_name="Conductividad Térmica (W/mK)")
    
    def __str__(self):
        return f"{self.nombre} ({self.conductividad} W/mK)"

class TipoProyecto(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

# ----------------------------------------
# 2. ENTIDAD BASE CON RELACIÓN (REQUISITO 3)
# ----------------------------------------

class Cliente(models.Model):
    """
    Entidad para representar al cliente/propietario de la vivienda.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre/Razón Social")
    contacto = models.CharField(max_length=100, verbose_name="Email de Contacto", unique=True)
    
    def __str__(self):
        return self.nombre # <-- Importante para el selector del formulario

# ----------------------------------------
# 3. ENTIDAD RELACIONADA N:M (REQUISITO 3)
# ----------------------------------------

class SistemaClimatizacion(models.Model):
    """
    Sistemas de climatización que puede tener el proyecto. Usado en relación N:M.
    """
    tipo = models.CharField(max_length=100, verbose_name="Tipo de Sistema")
    eficiencia_nominal = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, verbose_name="Eficiencia Nominal (COP/SCOP)")
    
    def __str__(self):
        return f"{self.tipo} (Eficiencia: {self.eficiencia_nominal})"

# ----------------------------------------
# 4. ENTIDAD PRINCIPAL: PROYECTO
# ----------------------------------------

class Proyecto(models.Model):
    """
    Modelo principal que representa la Vivienda o el Proyecto de Calificación Energética.
    """
    # Relación 1:N (ForeignKey) - REQUISITO 3
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='proyectos')
    tipo = models.ForeignKey(TipoProyecto, on_delete=models.PROTECT)

    # Campos de datos
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la Vivienda/Proyecto")
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField(default=date.today)

    # Relación N:M (ManyToManyField) - REQUISITO 3
    sistemas = models.ManyToManyField(SistemaClimatizacion, related_name='proyectos')

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"

    def get_estado_display(self):
        # Simulación de un campo de estado para visualización
        if self.resultados.exists():
            return f"Calificado ({self.resultados.first().calificacion})"
        return "En Curso"

# ----------------------------------------
# 5. ENTIDAD RELACIONADA 1:1 (REQUISITO 3)
# ----------------------------------------

class ResultadoCEV(models.Model):
    """
    Almacena la calificación final del proyecto (Relación 1:1).
    """
    CALIFICACIONES = (
        ('A+', 'A+ (Excelente)'),
        ('A', 'A (Muy Bueno)'),
        ('B', 'B (Bueno)'),
        ('C', 'C (Estándar)'),
        ('D', 'D (Malo)'),
    )
    # Relación 1:1 (OneToOneField) - REQUISITO 3
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE, related_name='resultados')
    calificacion = models.CharField(max_length=2, choices=CALIFICACIONES)
    consumo_energia_anual = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Consumo Anual (kWh/m²)")
    fecha_calificacion = models.DateField(default=date.today)

    def __str__(self):
        return f"Resultado de {self.proyecto.nombre}: {self.calificacion}"

# ----------------------------------------
# 6. ENTIDAD RELACIONADA 1:N (REQUISITO 3)
# ----------------------------------------

class Muro(models.Model):
    """
    Componente de la envolvente (muros, techos) asociado a un proyecto (Relación 1:N).
    """
    # Relación 1:N (ForeignKey) - REQUISITO 3
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='muros')
    
    # Relación 1:N al Material (el aislante usado)
    material_aislante = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='muros')

    ubicacion = models.CharField(max_length=50, verbose_name="Ubicación (Norte, Sur, etc.)")
    superficie = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Superficie (m²)")
    
    def __str__(self):
        return f"Muro {self.ubicacion} del Proyecto {self.proyecto.nombre}"