from flask import Flask, abort, redirect, render_template, url_for
from models import Base, Task, engine, wait_for_db, SessionLocal, User
from flask_login import LoginManager, login_required, current_user
from flask_wtf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix
from auth import auth_bp
from tasks import tasks_bp
from logging.handlers import RotatingFileHandler
import os
import logging

def create_app():
    app = Flask(__name__)

    # Configuración Auditoria: Registro de errores y eventos en un archivo que rota al alcanzar 1MB
    handler = RotatingFileHandler('security_audit.log', maxBytes=1000000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s [IP: %(remote_addr)s]')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)    
    
    # Inyeccion de IP en los logs para tener trazabilidad de eventos por dirección IP
    @app.before_request
    def log_request_info():
        from flask import request
        request.remote_addr = request.headers.get('X-Real-IP)', request.remote_addr)
    
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev_key')
    
    # Configuración de Cookies Seguras (ahora que tenemos HTTPS)
    app.config.update(
        SESSION_COOKIE_SECURE=True,   
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )

    # Indica a Flask que confíe en el Proxy (Nginx)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # Activar CSRF de forma global
    csrf = CSRFProtect(app)

    # Esperar a la BD y crear tablas
    wait_for_db(engine)
    Base.metadata.create_all(bind=engine)

    # Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        db = SessionLocal()
        user = db.query(User).get(int(user_id))
        db.close()
        return user

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    # Rutas
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return redirect(url_for("tasks.list_tasks"))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000) #nosec