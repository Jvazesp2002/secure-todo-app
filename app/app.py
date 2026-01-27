from flask import Flask
from models import Base, engine, wait_for_db
import os

def create_app():
    app = Flask(__name__)

    # Configuración básica
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev_key')
    
    # Crea tablas al arrancar la aplicación
    wait_for_db(engine)
    Base.metadata.create_all(bind=engine)
    
    
    @app.route('/')
    def index():
        return "Flask esta corriendo correctamente."
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)