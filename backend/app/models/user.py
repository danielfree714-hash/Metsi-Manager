from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Credenciales
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Estado
    is_active = Column(Boolean, default=True)

    # Relaciones
    team = relationship("Team", back_populates="user", uselist=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
