
# 🏡 SAAS CEV — Sistema de Calificación Energética de Viviendas

Aplicación web desarrollada en **Django** para gestionar el proceso completo de **Calificación Energética de Viviendas (CEV)**: registro de proyectos, gestión de clientes, materiales, sistemas de climatización, envolventes térmicas y resultados de certificación.




## 🎯 Propósito del Sistema

El objetivo del sistema es centralizar y automatizar la información necesaria para evaluar viviendas según criterios de eficiencia energética. Permite:

* Gestión de proyectos de distintas tipologías
* Administración de clientes
* Control de materiales aislantes y su conductividad térmica
* Registro de sistemas de climatización
* Análisis de componentes de envolvente: muros, techumbres, superficies
* Cálculo y almacenamiento de calificaciones energéticas (A+, A, B, C, D)

---

## 🚀 Tecnologías Utilizadas

* **Python 3.x**
* **Django 4.x – 5.x**
* **Django ORM**
* **SQLite (dev)** / PostgreSQL (producción)
* **Class-Based Views (CBV)**
* **Django Admin con Inlines**

---

## 📦 Requisitos Previos

* Python 3.8+
* pip instalado
* Entorno virtual recomendado (venv, virtualenv o pipenv)

---

## 🔧 Instalación y Configuración

### 1️⃣ Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd SAAS-CEV
```

### 2️⃣ Crear y activar el entorno virtual

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

Si no existe `requirements.txt`:

```bash
pip install django
```

### 4️⃣ Preparar base de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Crear superusuario

```bash
python manage.py createsuperuser
```

### 6️⃣ Ejecutar el servidor

```bash
python manage.py runserver
```

La aplicación estará disponible en:
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📁 Estructura del Proyecto

```
CEVProject/
├── gestion/                 # App principal
│   ├── migrations/
│   ├── templates/
│   │   └── gestion/
│   ├── admin.py             # Panel admin personalizado
│   ├── models.py            # Modelos de datos
│   ├── views.py             # Vistas CBV (CRUD completo)
│   ├── urls.py
│   └── tests.py
│
├── CEVProject/              # Proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---

## 🗄️ Modelos Principales

### **1. Material**

Material aislante y su conductividad térmica.
Campos: `nombre`, `conductividad`

### **2. TipoProyecto**

Clasificación del proyecto.
Campos: `nombre`

### **3. Cliente**

Propietario o entidad responsable.
Campos: `nombre`, `contacto`

### **4. SistemaClimatizacion**

Equipos de calefacción/refrigeración.
Campos: `tipo`, `eficiencia_nominal`

### **5. Proyecto**

Entidad principal del sistema.
Relaciones: Cliente, Tipo, Muros, Sistemas, ResultadoCEV

### **6. Muro**

Componentes de la envolvente.
Campos: `ubicacion`, `superficie`, `material`

### **7. ResultadoCEV**

Calificación energética final.
Campos: `calificacion`, `consumo_energia_anual`

---

## 🎨 Interfaz y Funcionalidades

### 🔑 Panel de Administración

`/admin/`

Incluye:

* Inlines para editar Muros y Resultados directamente dentro del Proyecto
* Fieldsets organizados
* Búsqueda, filtros y date hierarchy
* Creación rápida de Clientes y Tipos desde pop-ups

---

### 🌐 Interfaz Pública (CRUD)

| Acción           | URL                         | Descripción               |
| ---------------- | --------------------------- | ------------------------- |
| Home             | `/`                         | Vista principal           |
| Listar Proyectos | `/proyectos/`               | Lista con filtros y orden |
| Detalle          | `/proyectos/<id>/`          | Información completa      |
| Crear            | `/proyectos/crear/`         | Formulario de ingreso     |
| Editar           | `/proyectos/<id>/editar/`   | Actualización             |
| Eliminar         | `/proyectos/<id>/eliminar/` | Confirmación              |

---

## 🧠 Técnicas Usadas

### 🔍 ORM Avanzado

```python
proyectos_recientes = Proyecto.objects.filter(
    fecha_inicio__gte=first_day_of_month
).order_by('-fecha_inicio')
```

### 🧱 Relaciones

* 1:N (ForeignKey)
* N:M (ManyToMany)
* 1:1 (OneToOne)

### 🧪 Tests

```bash
python manage.py test gestion
```

---

## 🔐 Recomendaciones para Producción

* `DEBUG = False`
* Cambiar `SECRET_KEY`
* Configurar `ALLOWED_HOSTS`
* Migrar a PostgreSQL
* Servir estáticos con Nginx
* HTTPS obligatorio
* Variables de entorno

---

## 🐛 Solución de Problemas Comunes

**Error: No module named 'django'**

```bash
pip install django
```

**Error en migraciones**

```bash
python manage.py makemigrations gestion
python manage.py migrate
```

**Puerto ocupado**

```bash
python manage.py runserver 8080
```

---

## 📅 Roadmap / Mejoras Futuras

* [ ] Cálculo automático de transmitancia térmica
* [ ] Generación de informes PDF
* [ ] Dashboard con gráficos de consumo
* [ ] Sistema de usuarios y roles
* [ ] API REST (Django REST Framework)
* [ ] UI con Bootstrap/Tailwind
* [ ] Notificaciones
* [ ] Búsqueda avanzada
* [ ] Comparación entre proyectos

---

## 👤 Autor

Proyecto desarrollado como parte del **Módulo M8 – Proyecto Final Talento Digital**
**Última actualización:** Noviembre 2025
**Versión:** 1.0.0


<<<<<<< HEAD
=======
  * `gestion/models.py`: Modelos con las relaciones complejas (Req. 2 y 3).
  * `gestion/views.py`: Lógica CRUD y Consulta ORM (`ProyectoListView` - Req. 5 y 6).
  * `gestion/admin.py`: Configuración del panel de administración (Req. 7).
  * `requirements.txt`: Lista de dependencias del proyecto.
  * `.gitignore`: Asegura que `db.sqlite3` y `venv/` no se suban al repositorio.
>>>>>>> 2f3fe97a51806ce7124469df65c3633721b685fa
