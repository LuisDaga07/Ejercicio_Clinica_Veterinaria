from flask import current_app
from flaskext.mysql import MySQL
from contextlib import contextmanager
from werkzeug.security import check_password_hash

class Database:
    """Clase para manejo de conexiones a la base de datos"""
    
    def __init__(self, app=None):
        self.mysql = MySQL()
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializar la aplicación con la configuración de MySQL"""
        app.config['MYSQL_DATABASE_HOST'] = app.config.get('MYSQL_DATABASE_HOST', 'localhost')
        app.config['MYSQL_DATABASE_USER'] = app.config.get('MYSQL_DATABASE_USER', 'root')
        app.config['MYSQL_DATABASE_PASSWORD'] = app.config.get('MYSQL_DATABASE_PASSWORD', '')
        app.config['MYSQL_DATABASE_DB'] = app.config.get('MYSQL_DATABASE_DB', 'sistema_veterinario')
        
        self.mysql.init_app(app)
    
    @contextmanager
    def get_connection(self):
        """Context manager para obtener conexión a la base de datos"""
        connection = None
        try:
            connection = self.mysql.connect()
            yield connection
        except Exception as e:
            current_app.logger.error(f"Error de conexión a la BD: {e}")
            raise
        finally:
            if connection:
                connection.close()

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Ejecutar consulta SQL con manejo de errores"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            try:
                print(f"Ejecutando consulta: {query}")
                print(f"Con parámetros: {params}")
                cursor.execute(query, params or ())
                if fetch_one:
                    result = cursor.fetchone()
                elif fetch_all:
                    result = cursor.fetchall()
                else:
                    connection.commit()
                    result = cursor.rowcount
                print(f"Resultado: {result}")
                return result
            except Exception as e:
                current_app.logger.error(f"Error ejecutando consulta: {e}")
                raise
            finally:
                cursor.close()

    @classmethod
    def authenticate(cls, email, password):
        query = "SELECT * FROM admin WHERE email = %s"
        try:
            result = db.execute_query(query, (email,), fetch_one=True)
            print(f"Resultado de la consulta: {result}")
            if result:
                print(f"Password ingresada: {password}")
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

# Instancia global de la base de datos
db = Database()