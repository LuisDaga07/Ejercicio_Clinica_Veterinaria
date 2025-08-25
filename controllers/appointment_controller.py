from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.appointment import Appointment
from services.validation_service import ValidationService

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/', methods=['GET', 'POST'])
def index():
    """Página principal con formulario de citas"""
    mesage = ''
    
    if request.method == 'POST':
        # Obtener y sanitizar datos del formulario
        mascota = ValidationService.sanitize_input(request.form.get('txtMascota'))
        edad = ValidationService.sanitize_input(request.form.get('txtEdad'))
        raza = ValidationService.sanitize_input(request.form.get('txtRaza'))
        fecha = request.form.get('txtFecha')
        hora = request.form.get('txtHora')
        amo = ValidationService.sanitize_input(request.form.get('txtAmo'))
        
        # Validar datos
        errors = ValidationService.validate_appointment_data(mascota, edad, raza, fecha, hora, amo)
        
        if errors:
            mesage = '; '.join(errors)
        else:
            # Verificar disponibilidad
            if Appointment.check_availability(fecha, hora):
                # Crear la cita
                if Appointment.create(mascota, edad, raza, fecha, hora, amo):
                    mesage = 'Su Cita ha Sido Agendada Satisfactoriamente!'
                else:
                    mesage = 'Error al procesar la solicitud. Intente nuevamente.'
            else:
                mesage = 'Horario no Disponible, Por Favor Agende un Horario Disponible!'
    
    return render_template('paginaWeb/index.html', mesage=mesage)

@appointment_bp.route('/service')
def servicios():
    """Página de servicios"""
    return render_template('paginaWeb/servicios.html')

@appointment_bp.route('/lista_usuario')
def lista_usuarios():
    """Lista de citas (solo para administradores)"""
    if not session.get('loggedin'):
        return redirect(url_for('appointment.index'))
    
    try:
        usuarios = Appointment.get_all()
        return render_template('admin/lista_user.html', usuarios=usuarios)
    except Exception as e:
        flash('Error al cargar la lista de usuarios', 'error')
        return redirect(url_for('appointment.index'))

@appointment_bp.route('/edit/<int:id>')
def edit_appointment(id):
    """Editar cita (solo para administradores)"""
    if not session.get('loggedin'):
        return redirect(url_for('appointment.index'))
    
    try:
        appointment = Appointment.get_by_id(id)
        if not appointment:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('appointment.lista_usuarios'))
        
        return render_template('admin/editar.html', usuarios=[appointment])
    except Exception as e:
        flash('Error al cargar el usuario', 'error')
        return redirect(url_for('appointment.lista_usuarios'))

@appointment_bp.route('/update', methods=['POST'])
def update_appointment():
    """Actualizar cita (solo para administradores)"""
    if not session.get('loggedin'):
        return redirect(url_for('appointment.index'))
    
    # Obtener y sanitizar datos
    mascota = ValidationService.sanitize_input(request.form.get('txtMascota'))
    edad = ValidationService.sanitize_input(request.form.get('txtEdad'))
    raza = ValidationService.sanitize_input(request.form.get('txtRaza'))
    fecha = request.form.get('txtFecha')
    hora = request.form.get('txtHora')
    amo = ValidationService.sanitize_input(request.form.get('txtAmo'))
    appointment_id = request.form.get('txtID')
    
    if not appointment_id:
        flash('ID de cita no válido', 'error')
        return redirect(url_for('appointment.lista_usuarios'))
    
    # Validar datos
    errors = ValidationService.validate_appointment_data(mascota, edad, raza, fecha, hora, amo)
    
    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect(url_for('appointment.edit_appointment', id=appointment_id))
    
    try:
        # Verificar disponibilidad (excluyendo la cita actual)
        if not Appointment.check_availability(fecha, hora, appointment_id):
            flash('Horario no disponible, por favor elija otro horario', 'error')
            return redirect(url_for('appointment.edit_appointment', id=appointment_id))
        
        # Obtener la cita y actualizarla
        appointment = Appointment.get_by_id(appointment_id)
        if not appointment:
            flash('Cita no encontrada', 'error')
            return redirect(url_for('appointment.lista_usuarios'))
        
        if appointment.update(mascota, edad, raza, fecha, hora, amo):
            flash('Usuario actualizado exitosamente', 'success')
        else:
            flash('Error al actualizar el usuario', 'error')
            
    except Exception as e:
        flash('Error al actualizar el usuario', 'error')
    
    return redirect(url_for('appointment.lista_usuarios'))

@appointment_bp.route("/destroy/<int:id>")
def destroy_appointment(id):
    """Eliminar cita (solo para administradores)"""
    if not session.get('loggedin'):
        return redirect(url_for('appointment.index'))
    
    try:
        appointment = Appointment.get_by_id(id)
        if not appointment:
            flash('Cita no encontrada', 'error')
        elif appointment.delete():
            flash('Usuario eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar el usuario', 'error')
    except Exception as e:
        flash('Error al eliminar el usuario', 'error')
    
    return redirect(url_for('appointment.lista_usuarios')) 