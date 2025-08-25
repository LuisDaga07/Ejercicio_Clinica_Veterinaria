# 🏥 Sistema de Citas Veterinarias

Un sistema web moderno para la gestión de citas veterinarias, desarrollado con Flask y MySQL.

## 🚀 Características

- ✅ **Agendar citas** de mascotas con validaciones
- ✅ **Panel administrativo** para gestionar citas
- ✅ **Interfaz moderna** y responsive
- ✅ **Validaciones robustas** de formularios
- ✅ **Sistema de autenticación** para administradores
- ✅ **Diseño profesional** con colores veterinarios

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python Flask
- **Base de Datos**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Iconos**: Font Awesome
- **Fuentes**: Google Fonts (Inter)
- **Servidor**: XAMPP (MySQL)

## 🏗️ Arquitectura del Proyecto

### Patrón MVC (Model-View-Controller)
- **Models**: Lógica de datos y acceso a base de datos
- **Views**: Plantillas HTML y presentación
- **Controllers**: Lógica de negocio y manejo de rutas

### Factory Pattern
- Configuración modular para diferentes entornos
- Inicialización limpia de la aplicación Flask

### Service Layer
- Separación de lógica de validación
- Reutilización de código de negocio

## 📋 Requisitos Previos

- Python 3.7+
- XAMPP (para MySQL)
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/sistema-veterinario.git
cd sistema-veterinario
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar la base de datos
Sigue las instrucciones en [INSTRUCCIONES_BASE_DATOS.md](INSTRUCCIONES_BASE_DATOS.md)

### 4. Ejecutar la aplicación
```bash
python app.py
```

## 🌐 Acceso a la Aplicación

- **Sitio web**: http://127.0.0.1:5000
- **Panel admin**: http://127.0.0.1:5000/inicio/login_

### Credenciales por defecto:
- **Email**: `admin@veterinario.com`
- **Usuario**: `admin`
- **Contraseña**: `admin123`

## 📁 Estructura del Proyecto

```
sistema-veterinario/
├── app.py                      # Aplicación principal Flask (Factory Pattern)
├── config.py                   # Configuración de la aplicación
├── db.py                       # Configuración de base de datos (compatibilidad)
├── requirements.txt            # Dependencias de Python
├── INSTRUCCIONES_BASE_DATOS.md # Instrucciones de configuración
├── models/                     # Modelos de datos (MVC)
│   ├── __init__.py
│   ├── database.py            # Clase de manejo de base de datos
│   ├── appointment.py         # Modelo de citas
│   └── admin.py               # Modelo de administradores
├── controllers/                # Controladores (MVC)
│   ├── __init__.py
│   ├── appointment_controller.py # Controlador de citas
│   └── auth_controller.py     # Controlador de autenticación
├── services/                   # Servicios de negocio
│   ├── __init__.py
│   └── validation_service.py  # Servicio de validaciones
├── static/                     # Archivos estáticos
│   ├── css/
│   │   ├── style.css          # Estilos principales
│   │   └── img/               # Imágenes
│   └── js/
│       └── main.js            # JavaScript
├── templates/                  # Plantillas HTML (Vistas MVC)
│   ├── admin/                 # Panel administrativo
│   │   ├── admin.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── lista_user.html
│   │   └── editar.html
│   ├── paginaWeb/             # Páginas públicas
│   │   ├── index.html
│   │   └── servicios.html
│   ├── errors/                # Páginas de error
│   │   ├── 404.html
│   │   └── 500.html
│   ├── header.html
│   └── footer.html
└── views/                      # Rutas legacy (mantenimiento)
    └── roles.py               # Rutas de autenticación
```

## 🎨 Características del Diseño

### Paleta de Colores
- **Primario**: Azul (#2563eb)
- **Secundario**: Azul oscuro (#1e40af)
- **Acento**: Naranja (#f59e0b)
- **Éxito**: Verde (#10b981)
- **Error**: Rojo (#ef4444)

### Funcionalidades
- **Formulario de citas** con validaciones en tiempo real
- **Panel administrativo** con dashboard moderno
- **Gestión de citas** (ver, editar, eliminar)
- **Responsive design** para móviles y tablets
- **Animaciones suaves** y transiciones

## 🔒 Seguridad

- Validación de sesiones para panel administrativo
- Sanitización de datos de entrada
- Validaciones de formularios en frontend y backend
- Protección contra SQL injection
- Manejo seguro de contraseñas

## 🚀 Funcionalidades Principales

### Para Clientes
- Agendar citas para mascotas
- Ver información del centro veterinario
- Formulario de contacto

### Para Administradores
- Dashboard con estadísticas
- Gestión completa de citas
- Panel de usuarios
- Sistema de autenticación

## 📱 Responsive Design

La aplicación está optimizada para:
- 📱 Móviles (320px+)
- 📱 Tablets (768px+)
- 💻 Escritorio (1024px+)

## 🐛 Solución de Problemas

### Error de conexión a MySQL
1. Verifica que XAMPP esté ejecutándose
2. Confirma que MySQL esté iniciado
3. Revisa la configuración en `app.py`

### Error de base de datos no encontrada
1. Sigue las instrucciones de configuración
2. Verifica que la base de datos exista
3. Confirma el nombre exacto

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- Flask por el framework web
- Font Awesome por los iconos
- Google Fonts por las tipografías
- La comunidad de desarrolladores

---

⭐ **Si te gusta este proyecto, dale una estrella en GitHub!** 