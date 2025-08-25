
import os
from flask import Flask, render_template
from config import config
from models.database import db
from controllers.appointment_controller import appointment_bp
from controllers.auth_controller import auth_bp

def create_app(config_name='default'):
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(appointment_bp)
    app.register_blueprint(auth_bp)
    
    # Manejo de errores
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    """Registrar manejadores de errores"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

if __name__ == '__main__':
    # Obtener configuración del entorno
    config_name = os.environ.get('FLASK_CONFIG') or 'default'
    app = create_app(config_name)
    
    app.run(debug=app.config.get('DEBUG', True), port=5000)