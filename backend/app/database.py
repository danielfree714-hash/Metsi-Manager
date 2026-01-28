from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# -------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------

# Render / Producción usará DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback para desarrollo local
if DATABASE_URL is None:
    DATABASE_URL = "sqlite:///./metsi_manager.db"

# Ajuste especial para PostgreSQL (Render)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# -------------------------------------------------
# ENGINE
# -------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True
)

# -------------------------------------------------
# SESIÓN
# -------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -------------------------------------------------
# BASE PARA MODELOS
# -------------------------------------------------

Base = declarative_base()

# -------------------------------------------------
# DEPENDENCIA PARA FASTAPI
# -------------------------------------------------

def get_db():
    """
    Generador de sesión para FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
