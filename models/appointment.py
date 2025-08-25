from datetime import datetime
from models.database import db

class Appointment:
    """Modelo para las citas veterinarias"""
    
    def __init__(self, id=None, mascota=None, edad=None, raza=None, 
                 fecha=None, hora=None, amo=None, created_at=None, updated_at=None):
        self.id = id
        self.mascota = mascota
        self.edad = edad
        self.raza = raza
        self.fecha = fecha
        self.hora = hora
        self.amo = amo
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def create(cls, mascota, edad, raza, fecha, hora, amo):
        """Crear una nueva cita"""
        query = """
        INSERT INTO usuarios (mascota, edad, raza, fecha, hora, amo) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (mascota, edad, raza, fecha, hora, amo)
        
        try:
            db.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error creando cita: {e}")
            return False
    
    @classmethod
    def get_all(cls):
        """Obtener todas las citas ordenadas por fecha y hora"""
        query = "SELECT * FROM usuarios ORDER BY fecha DESC, hora ASC"
        
        try:
            results = db.execute_query(query, fetch_all=True)
            appointments = []
            for row in results:
                appointment = cls(
                    id=row[0],
                    mascota=row[1],
                    edad=row[2],
                    raza=row[3],
                    fecha=row[4],
                    hora=row[5],
                    amo=row[6],
                    created_at=row[7],
                    updated_at=row[8]
                )
                appointments.append(appointment)
            return appointments
        except Exception as e:
            print(f"Error obteniendo citas: {e}")
            return []
    
    @classmethod
    def get_by_id(cls, appointment_id):
        """Obtener una cita por ID"""
        query = "SELECT * FROM usuarios WHERE id = %s"
        
        try:
            result = db.execute_query(query, (appointment_id,), fetch_one=True)
            if result:
                return cls(
                    id=result[0],
                    mascota=result[1],
                    edad=result[2],
                    raza=result[3],
                    fecha=result[4],
                    hora=result[5],
                    amo=result[6],
                    created_at=result[7],
                    updated_at=result[8]
                )
            return None
        except Exception as e:
            print(f"Error obteniendo cita: {e}")
            return None
    
    @classmethod
    def check_availability(cls, fecha, hora, exclude_id=None):
        """Verificar si un horario está disponible"""
        if exclude_id:
            query = "SELECT * FROM usuarios WHERE fecha = %s AND hora = %s AND id != %s"
            params = (fecha, hora, exclude_id)
        else:
            query = "SELECT * FROM usuarios WHERE fecha = %s AND hora = %s"
            params = (fecha, hora)
        
        try:
            result = db.execute_query(query, params, fetch_one=True)
            return result is None  # True si está disponible
        except Exception as e:
            print(f"Error verificando disponibilidad: {e}")
            return False
    
    def update(self, mascota, edad, raza, fecha, hora, amo):
        """Actualizar una cita existente"""
        query = """
        UPDATE usuarios 
        SET mascota = %s, edad = %s, raza = %s, fecha = %s, hora = %s, amo = %s 
        WHERE id = %s
        """
        params = (mascota, edad, raza, fecha, hora, amo, self.id)
        
        try:
            db.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error actualizando cita: {e}")
            return False
    
    def delete(self):
        """Eliminar una cita"""
        query = "DELETE FROM usuarios WHERE id = %s"
        
        try:
            db.execute_query(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error eliminando cita: {e}")
            return False
    
    @classmethod
    def count(cls):
        """Contar el total de citas"""
        query = "SELECT COUNT(*) FROM usuarios"
        
        try:
            result = db.execute_query(query, fetch_one=True)
            return result[0] if result else 0
        except Exception as e:
            print(f"Error contando citas: {e}")
            return 0
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'mascota': self.mascota,
            'edad': self.edad,
            'raza': self.raza,
            'fecha': self.fecha,
            'hora': self.hora,
            'amo': self.amo,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 