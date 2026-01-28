from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    # -------------------------
    # IDENTIDAD
    # -------------------------
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # -------------------------
    # ESTADO
    # -------------------------
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # -------------------------
    # RELACIONES
    # -------------------------
    teams = relationship("Team", back_populates="owner")

    # -------------------------
    # METADATA
    # -------------------------
    created_at = Column(DateTime(timezone=True), server_default=func.now())
