# SAAS CEV - Sistema de Calificación Energética de Viviendas

## 📋 Descripción del Proyecto

SAAS CEV es una aplicación web desarrollada con Django que permite gestionar proyectos de calificación energética de viviendas, controlando materiales, sistemas de climatización, componentes de envolvente y resultados de calificación energética según estándares de eficiencia.

## 🎯 Objetivo del Sistema

Facilitar la gestión integral de proyectos de certificación energética, permitiendo:
- Registro y seguimiento de proyectos de viviendas
- Gestión de clientes y tipos de proyecto
- Control de materiales aislantes y su conductividad térmica
- Registro de sistemas de climatización
- Análisis de componentes de envolvente (muros, techos)
- Almacenamiento de resultados de calificación energética (A+, A, B, C, D)

## 🚀 Tecnologías Utilizadas

- **Framework**: Django 4.x
- **Lenguaje**: Python 3.x
- **Base de datos**: SQLite3 (desarrollo)
- **ORM**: Django ORM con consultas avanzadas
- **Vistas**: Class-Based Views (CBV)
- **Admin**: Django Admin personalizado con Inlines

## 📦 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Entorno virtual (recomendado)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone [URL_DEL_REPOSITORIO]
cd SAAS-CEV
```

### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install django
```

O si existe `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://127.0.0.1:8000/`

## 📁 Estructura del Proyecto

```
CEVProject/
│
├── gestion/                 # Aplicación principal
│   ├── migrations/          # Migraciones de base de datos
│   ├── templates/           # Templates HTML
│   │   └── gestion/
│   │       ├── home.html
│   │       ├── proyecto_list.html
│   │       ├── proyecto_detail.html
│   │       ├── proyecto_form.html
│   │       └── proyecto_confirm_delete.html
│   ├── admin.py            # Configuración del panel admin
│   ├── models.py           # 7 modelos de datos
│   ├── views.py            # Vistas CBV (CRUD completo)
│   ├── urls.py             # URLs de la aplicación
│   └── tests.py            # Tests unitarios
│
├── CEVProject/              # Configuración del proyecto
│   ├── settings.py         # Configuración general
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # Configuración WSGI
│
├── db.sqlite3              # Base de datos SQLite
├── manage.py               # Gestor del proyecto Django
└── requirements.txt        # Dependencias del proyecto
```

## 🗄️ Modelos de Datos

### 1. Material
Almacena materiales aislantes con sus propiedades térmicas.

**Campos:**
- `nombre` (CharField): Identificador del material
- `conductividad` (DecimalField): Conductividad térmica en W/mK

### 2. TipoProyecto
Clasificación de proyectos (Residencial, Comercial, etc.)

**Campos:**
- `nombre` (CharField): Tipo de proyecto

### 3. Cliente
Propietarios o responsables de las viviendas.

**Campos:**
- `nombre` (CharField): Nombre o razón social
- `contacto` (CharField): Email único de contacto

**Relación:**
- 1:N → Proyectos

### 4. SistemaClimatizacion
Sistemas de calefacción/refrigeración.

**Campos:**
- `tipo` (CharField): Tipo de sistema
- `eficiencia_nominal` (DecimalField): COP/SCOP

**Relación:**
- N:M ↔ Proyectos

### 5. Proyecto (Principal)
Representa cada vivienda o proyecto de certificación.

**Campos:**
- `nombre` (CharField): Nombre del proyecto
- `descripcion` (TextField): Descripción detallada
- `fecha_inicio` (DateField): Fecha de inicio

**Relaciones:**
- N:1 → Cliente
- N:1 → TipoProyecto
- N:M ↔ SistemaClimatizacion
- 1:1 ↔ ResultadoCEV
- 1:N → Muros

### 6. Muro
Componentes de la envolvente térmica.

**Campos:**
- `ubicacion` (CharField): Orientación (Norte, Sur, etc.)
- `superficie` (DecimalField): Área en m²

**Relaciones:**
- N:1 → Proyecto
- N:1 → Material (aislante utilizado)

### 7. ResultadoCEV
Calificación energética final del proyecto.

**Campos:**
- `calificacion` (CharField): A+, A, B, C, D
- `consumo_energia_anual` (DecimalField): kWh/m²
- `fecha_calificacion` (DateField): Fecha de evaluación

**Relación:**
- 1:1 → Proyecto

## 🎯 Funcionalidades Implementadas

### Panel de Administración Django

**URL:** `http://127.0.0.1:8000/admin/`

Características avanzadas:
- ✅ Gestión completa de todos los modelos
- ✅ **Inlines** para editar Muros y Resultados dentro de Proyecto
- ✅ **Fieldsets organizados** para mejor UX
- ✅ **List display** personalizado con filtros
- ✅ **Search fields** para búsqueda rápida
- ✅ **Date hierarchy** para navegación temporal
- ✅ **Pop-ups** automáticos para crear Clientes/Tipos desde formulario

### Vistas Públicas (CRUD Completo)

#### Home
- **URL:** `/`
- **Descripción:** Página principal del sistema

#### Listar Proyectos
- **URL:** `/proyectos/`
- **Descripción:** Lista todos los proyectos con consulta ORM avanzada
- **Extra:** Muestra proyectos iniciados en el mes actual

#### Ver Detalle
- **URL:** `/proyectos/<id>/`
- **Descripción:** Muestra información completa de un proyecto

#### Crear Proyecto
- **URL:** `/proyectos/crear/`
- **Descripción:** Formulario para registrar nuevo proyecto

#### Editar Proyecto
- **URL:** `/proyectos/<id>/editar/`
- **Descripción:** Actualizar información de proyecto existente

#### Eliminar Proyecto
- **URL:** `/proyectos/<id>/eliminar/`
- **Descripción:** Confirmación y eliminación de proyecto

## 💡 Características Técnicas Destacadas

### Consultas ORM Avanzadas
```python
# Filtro de proyectos por fecha
proyectos_recientes = Proyecto.objects.filter(
    fecha_inicio__gte=first_day_of_month
).order_by('-fecha_inicio')
```

### Class-Based Views
- ListView
- DetailView
- CreateView
- UpdateView
- DeleteView
- TemplateView

### Relaciones de Base de Datos
- **ForeignKey** (1:N)
- **OneToOneField** (1:1)
- **ManyToManyField** (N:M)

### Admin Personalizado
- TabularInline para Muros
- StackedInline para ResultadoCEV
- Filtros y búsqueda optimizados

## 📝 Uso del Sistema

### 1. Registrar un Cliente
1. Acceder al admin: `/admin/`
2. Ir a "Clientes" → "Agregar Cliente"
3. Completar nombre y email
4. Guardar

### 2. Crear un Proyecto
**Opción A - Desde el Admin:**
1. Ir a "Proyectos" → "Agregar Proyecto"
2. Seleccionar cliente y tipo
3. Completar nombre, descripción y fecha
4. Agregar sistemas de climatización
5. Usar el inline para agregar muros
6. Guardar

**Opción B - Desde la Web:**
1. Ir a `/proyectos/crear/`
2. Llenar formulario
3. Enviar

### 3. Registrar Resultados
1. Editar un proyecto en el admin
2. Completar el inline "Resultado de Calificación Energética"
3. Seleccionar calificación (A+, A, B, C, D)
4. Ingresar consumo anual
5. Guardar

## 🧪 Ejecutar Tests

```bash
python manage.py test gestion
```

## 🔐 Configuración de Seguridad (Producción)

- [ ] Cambiar `SECRET_KEY` en `settings.py`
- [ ] Configurar `DEBUG = False`
- [ ] Definir `ALLOWED_HOSTS`
- [ ] Usar PostgreSQL o MySQL
- [ ] Configurar variables de entorno
- [ ] Habilitar HTTPS
- [ ] Configurar CSRF tokens

## 🐛 Solución de Problemas

### Error: "No module named 'django'"
```bash
pip install django
```

### Error en migraciones
```bash
python manage.py makemigrations gestion
python manage.py migrate
```

### Puerto ya en uso
```bash
python manage.py runserver 8080
```

## 📚 Documentación de Referencia

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Admin Customization](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- [Django Class-Based Views](https://docs.djangoproject.com/en/stable/topics/class-based-views/)

## 👤 Autor

**Proyecto desarrollado como parte del curso de desarrollo web**

- Módulo: M8 - Proyecto Final
- Institución: SkillNest
- Fecha: 2024/2025

## 📄 Licencia

Proyecto educativo - Todos los derechos reservados

## 🔄 Versión

**Versión actual**: 1.0.0  
**Última actualización**: Noviembre 2025

---

## 📌 Mejoras Futuras Planificadas

- [ ] Agregar cálculos automáticos de transmitancia térmica
- [ ] Implementar exportación de informes en PDF
- [ ] Crear dashboard con gráficos de consumo
- [ ] Agregar sistema de autenticación de usuarios
- [ ] Implementar API REST con Django REST Framework
- [ ] Agregar validaciones personalizadas en formularios
- [ ] Mejorar UI con Bootstrap o Tailwind CSS
- [ ] Implementar sistema de notificaciones
- [ ] Agregar búsqueda avanzada por múltiples criterios
- [ ] Crear módulo de comparación entre proyectos