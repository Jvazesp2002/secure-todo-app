import pytest
from app import create_app
from models import Base, engine, SessionLocal

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })

    Base.metadata.create_all(bind=engine)
    yield app
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_session():
    """Fixture para obtener una sesión de base de datos limpia en los tests."""
    session = SessionLocal()
    yield session
    session.close()