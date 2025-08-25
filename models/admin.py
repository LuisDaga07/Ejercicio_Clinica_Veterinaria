from models.database import db
import re
from werkzeug.security import generate_password_hash, check_password_hash

class Admin:
    """Modelo para administradores del sistema"""
    
    def __init__(self, id=None, email=None, usuario=None, password=None, 
                 created_at=None, updated_at=None):
        self.id = id
        self.email = email
        self.usuario = usuario
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def create(cls, email, usuario, password):
        """Crear un nuevo administrador"""
        hashed_password = generate_password_hash(password)
        query = """
        INSERT INTO admin (email, usuario, password) 
        VALUES (%s, %s, %s)
        """
        params = (email, usuario, hashed_password,)
        
        try:
            db.execute_query(query, params,)
            return True
        except Exception as e:
            print(f"Error creando administrador: {e}")
            return False
    
    @classmethod
    def authenticate(cls, email, password):
        """Autenticar un administrador"""
        query = "SELECT * FROM admin WHERE email = %s"
        
        try:
            result = db.execute_query(query, (email,), fetch_one=True)
            if result and check_password_hash(result[3], password):
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
    
    @classmethod
    def get_by_email(cls, email):
        """Obtener administrador por email"""
        query = "SELECT * FROM admin WHERE email = %s"
        
        try:
            result = db.execute_query(query, (email,), fetch_one=True)
            if result:
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
            print(f"Error obteniendo administrador: {e}")
            return None
    
    @classmethod
    def email_exists(cls, email):
        """Verificar si un email ya existe"""
        query = "SELECT * FROM admin WHERE email = %s"
        
        try:
            result = db.execute_query(query, (email,), fetch_one=True)
            return result is not None
        except Exception as e:
            print(f"Error verificando email: {e}")
            return False
    
    @staticmethod
    def validate_email(email):
        """Validar formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """Validar contraseña"""
        return len(password) >= 6
    
    def to_dict(self):
        """Convertir a diccionario (sin contraseña)"""
        return {
            'id': self.id,
            'email': self.email,
            'usuario': self.usuario,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }