from datetime import datetime
from flask import current_app

class ValidationService:
    """Servicio para validaciones de formularios"""
    
    @staticmethod
    def validate_date_format(date_str):
        """Validar formato de fecha YYYY-MM-DD"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_time_format(time_str):
        """Validar formato de hora HH:MM"""
        try:
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_future_date(date_str):
        """Validar que la fecha sea futura"""
        try:
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            today = datetime.now().date()
            return appointment_date >= today
        except ValueError:
            return False
    
    @staticmethod
    def validate_business_hours(time_str):
        """Validar horario de atención"""
        try:
            time_obj = datetime.strptime(time_str, '%H:%M').time()
            start_time = datetime.strptime(
                current_app.config.get('BUSINESS_HOURS_START', '08:00'), 
                '%H:%M'
            ).time()
            end_time = datetime.strptime(
                current_app.config.get('BUSINESS_HOURS_END', '20:00'), 
                '%H:%M'
            ).time()
            return start_time <= time_obj <= end_time
        except ValueError:
            return False
    
    @staticmethod
    def validate_pet_name(name):
        """Validar nombre de mascota"""
        min_length = current_app.config.get('MIN_PET_NAME_LENGTH', 2)
        return name and len(name.strip()) >= min_length
    
    @staticmethod
    def validate_owner_name(name):
        """Validar nombre del propietario"""
        min_length = current_app.config.get('MIN_OWNER_NAME_LENGTH', 3)
        return name and len(name.strip()) >= min_length
    
    @staticmethod
    def validate_appointment_data(mascota, edad, raza, fecha, hora, amo):
        """Validar todos los datos de una cita"""
        errors = []
        
        if not mascota or not mascota.strip():
            errors.append("El nombre de la mascota es requerido")
        elif not ValidationService.validate_pet_name(mascota):
            errors.append(f"El nombre de la mascota debe tener al menos {current_app.config.get('MIN_PET_NAME_LENGTH', 2)} caracteres")
        
        if not edad or not edad.strip():
            errors.append("La edad es requerida")
        
        if not raza or not raza.strip():
            errors.append("La raza es requerida")
        
        if not fecha:
            errors.append("La fecha es requerida")
        elif not ValidationService.validate_date_format(fecha):
            errors.append("Formato de fecha inválido. Use YYYY-MM-DD")
        elif not ValidationService.validate_future_date(fecha):
            errors.append("La fecha de la cita debe ser futura")
        
        if not hora:
            errors.append("La hora es requerida")
        elif not ValidationService.validate_time_format(hora):
            errors.append("Formato de hora inválido. Use HH:MM")
        elif not ValidationService.validate_business_hours(hora):
            errors.append(f"Horario de atención: {current_app.config.get('BUSINESS_HOURS_START', '08:00')} - {current_app.config.get('BUSINESS_HOURS_END', '20:00')}")
        
        if not amo or not amo.strip():
            errors.append("El nombre del propietario es requerido")
        elif not ValidationService.validate_owner_name(amo):
            errors.append(f"El nombre del propietario debe tener al menos {current_app.config.get('MIN_OWNER_NAME_LENGTH', 3)} caracteres")
        
        return errors
    
    @staticmethod
    def sanitize_input(text):
        """Sanitizar entrada de texto"""
        if not text:
            return ""
        return text.strip() 