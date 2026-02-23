import pytest
from app import create_app
from models import Base, engine, SessionLocal
import os

@pytest.fixture(scope="session") # Cambiamos a scope session para que sea más rápido
def app():
    # Seteamos variable de entorno para forzar modo test
    os.environ["FLASK_ENV"] = "testing"
    
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        # ESTA LÍNEA ES LA QUE EVITA EL CONGELAMIENTO:
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "PRESERVE_CONTEXT_ON_EXCEPTION": False
    })

    with app.app_context():
        Base.metadata.create_all(bind=engine)
        yield app
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        # Esto asegura que el test use la misma conexión que la app
        connection = engine.connect()
        transaction = connection.begin()
        session = SessionLocal(bind=connection)

        yield session

        session.close()
        transaction.rollback()
        connection.close()