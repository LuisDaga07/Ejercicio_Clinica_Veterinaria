from flask import(Blueprint, render_template, 
                  request, flash, redirect, url_for, session, current_app)
from werkzeug.security import check_password_hash
from models.admin import Admin
from services.validation_service import ValidationService
from models.database import db

auth_bp = Blueprint('auth', __name__, url_prefix='/inicio')

@auth_bp.route('/login_', methods=['GET', 'POST'])
def login():
    """Página de login"""
    mesage = ''
    if request.method == 'POST':
        email = request.form.get('txtEmail', '').strip()
        password = request.form.get('txtPassword', '').strip()
        if not email or not password:
            mesage = 'Por favor ingrese email y contraseña'
        else:
            try:
                admin = Admin.authenticate(email, password)
                if admin:
                    session['loggedin'] = True
                    session['id'] = admin.id
                    session['email'] = admin.email
                    session['usuario'] = admin.usuario
                    mesage = 'Inicio de sesión exitoso'
                    return render_template('admin/admin.html', mesage=mesage)
                else:
                    mesage = 'Email o contraseña incorrectos'
            except Exception as e:
                mesage = 'Error al iniciar sesión'
    return render_template('admin/login.html', mesage=mesage)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    mesage = ''
    if request.method == 'POST':
        email = ValidationService.sanitize_input(request.form.get('txtEmail'))
        usuario = ValidationService.sanitize_input(request.form.get('txtUsuario'))
        password = request.form.get('txtPassword', '')
        if not email or not usuario or not password:
            mesage = 'Por favor complete todos los campos'
        elif not Admin.validate_email(email):
            mesage = 'Formato de email inválido'
        elif not Admin.validate_password(password):
            mesage = 'La contraseña debe tener al menos 6 caracteres'
        else:
            try:
                if Admin.email_exists(email):
                    mesage = 'El email ya está registrado'
                else:
                    if Admin.create(email, usuario, password):
                        flash('Registro exitoso', 'success')
                        return redirect(url_for('auth.login'))
                    mesage = 'Error al crear la cuenta'
            except Exception as e:
                mesage = 'Error en el registro'
    return render_template('admin/register.html', mesage=mesage)

@auth_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    return redirect(url_for('appointment.index'))

@auth_bp.route('/admin')
def admin():
    """Panel de administración"""
    if not session.get('loggedin'):
        return redirect(url_for('appointment.index'))
    
    return render_template('admin/admin.html')

@auth_bp.route('/inicio')
def inicio():
    """Página de inicio del admin"""
    if not session.get('loggedin'):
        return redirect(url_for('appointment.index'))
    
    return render_template('admin/admin.html')

@classmethod
def authenticate(cls, email, password):
    query = "SELECT * FROM admin WHERE email = %s"
    try:
        result = db.execute_query(query, (email,), fetch_one=True)
        print(f"Email: {email}")
        print(f"Password ingresada: {password}")
        print(f"Resultado de la consulta: {result}")
        if result:
            print(f"Hash en BD: {result[3]}")
            print(f"check_password_hash: {check_password_hash(result[3], password)}")
            if check_password_hash(result[3], password):
                return cls(
                    id=result[0],
                    email=result[1],
                    usuario=result[2],
                    password=result[3],
                    created_at=result[4],
                    updated_at=result[5]
                )
        return None
    except Exception as e:
        print(f"Error autenticando administrador: {e}")
        return None