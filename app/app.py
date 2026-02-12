from flask import Flask, redirect, render_template, url_for
from models import Base, engine, wait_for_db, SessionLocal, User
from flask_login import LoginManager, login_required, current_user
from flask_wtf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix
from auth import auth_bp
from tasks import tasks_bp
import os

def create_app():
    app = Flask(__name__)

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
    app.run(host='0.0.0.0', port=5000)