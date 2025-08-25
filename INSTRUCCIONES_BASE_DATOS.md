# 🏥 Configuración de Base de Datos - Centro Veterinario

## 📋 Requisitos Previos

1. **XAMPP instalado** en tu computadora
2. **Python** con las dependencias instaladas
3. **Flask** y **Flask-MySQL** configurados

## 🚀 Pasos para Configurar la Base de Datos

### 1. **Iniciar XAMPP**
- Abre XAMPP Control Panel
- Inicia **Apache** y **MySQL**
- Verifica que ambos servicios estén ejecutándose (luz verde)

### 2. **Acceder a phpMyAdmin**
- Abre tu navegador
- Ve a: `http://localhost/phpmyadmin`
- Usuario: `root`
- Contraseña: (deja vacío si no configuraste contraseña)

### 3. **Crear la Base de Datos**
- En phpMyAdmin, haz clic en **"Nueva"** en el menú lateral
- Nombre de la base de datos: `sistema_veterinario`
- Cotejamiento: `utf8mb4_unicode_ci`
- Haz clic en **"Crear"**

### 4. **Crear las Tablas**

#### Tabla `usuarios` (para las citas):
```sql
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mascota VARCHAR(100) NOT NULL,
    edad VARCHAR(50) NOT NULL,
    raza VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    amo VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### Tabla `admin` (para administradores):
```sql
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    usuario VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 5. **Insertar Administrador por Defecto**
```sql
INSERT INTO admin (email, usuario, password) VALUES 
('admin@veterinario.com', 'admin', 'admin123');
```

### 6. **Crear Índices (Opcional pero Recomendado)**
```sql
CREATE INDEX idx_usuarios_fecha_hora ON usuarios(fecha, hora);
CREATE INDEX idx_admin_email ON admin(email);
```

## 🔧 Configuración de la Aplicación

### Verificar Configuración en `app.py`:
```python
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''  # Cambiar si tienes contraseña
app.config['MYSQL_DATABASE_DB'] = 'sistema_veterinario'
```

## 🚀 Ejecutar la Aplicación

1. **Instalar dependencias** (si no lo has hecho):
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación**:
   ```bash
   python app.py
   ```

3. **Acceder a la aplicación**:
   - Sitio web: `http://127.0.0.1:5000`
   - Panel admin: `http://127.0.0.1:5000/inicio/login_`

## 🔑 Credenciales por Defecto

- **Email**: `admin@veterinario.com`
- **Usuario**: `admin`
- **Contraseña**: `admin123`

## ⚠️ Solución de Problemas

### Error de Conexión a MySQL:
- Verifica que XAMPP esté ejecutándose
- Confirma que MySQL esté iniciado en XAMPP
- Revisa que el puerto 3306 esté disponible

### Error de Base de Datos No Encontrada:
- Verifica que la base de datos `sistema_veterinario` exista
- Confirma el nombre exacto de la base de datos

### Error de Tabla No Encontrada:
- Ejecuta los scripts SQL para crear las tablas
- Verifica que las tablas `usuarios` y `admin` existan

## 📝 Notas Importantes

- **Siempre mantén XAMPP ejecutándose** mientras uses la aplicación
- **Cambia la contraseña del administrador** después del primer login
- **Haz respaldos regulares** de la base de datos
- **La aplicación funciona en el puerto 5000** por defecto

## 🎯 Funcionalidades Disponibles

- ✅ Agendar citas de mascotas
- ✅ Panel administrativo
- ✅ Gestión de citas (ver, editar, eliminar)
- ✅ Validaciones de formularios
- ✅ Interfaz moderna y responsive 