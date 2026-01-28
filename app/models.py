from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_login import UserMixin
import os
import time

DB_USER = os.environ.get("MYSQL_USER")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD")
DB_HOST = os.environ.get("MYSQL_HOST")
DB_NAME = os.environ.get("MYSQL_DATABASE")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)

# Función para esperar a que la base de datos esté disponible

def wait_for_db(engine, retries=10, delay=3):
    for i in range(retries):
        try:
            connection = engine.connect()
            connection.close()
            print("✅ Base de datos Disponible")
            return
        except OperationalError:
            print(f"⏳ Esperando a la base de datos... ({i+1}/{retries})")
            time.sleep(delay)

    raise Exception("❌ Base de datos no disponible después de varios intentos.")


SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class User(UserMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)