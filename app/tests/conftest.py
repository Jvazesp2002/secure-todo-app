import pytest
from app import create_app
from models import Base, engine, SessionLocal, User, Task
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    # Crear la aplicación Flask para pruebas
    app = create_app()
    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield