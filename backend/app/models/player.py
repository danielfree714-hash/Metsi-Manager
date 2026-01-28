from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

from app.models.base import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)

    # Relación con equipo
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    team = relationship("Team", back_populates="players")

    # Identidad
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    position = Column(String(3), nullable=False)  # GK, DEF, MID, ATT

    # Habilidades (1–20)
    goalkeeping = Column(Integer, default=1)
    defense = Column(Integer, default=1)
    playmaking = Column(Integer, default=1)
    passing = Column(Integer, default=1)
    winger = Column(Integer, default=1)
    scoring = Column(Integer, default=1)
    set_pieces = Column(Integer, default=1)

    # Estado
    stamina = Column(Integer, default=5)
    form = Column(Integer, default=5)

    # Progresión
    seasons_played = Column(Integer, default=0)
    youth_product = Column(Boolean, default=False)

    # Progreso de entrenamiento por habilidad
    training_progress = Column(
        JSON,
        default={
            "goalkeeping": 0,
            "defense": 0,
            "playmaking": 0,
            "passing": 0,
            "winger": 0,
            "scoring": 0,
            "set_pieces": 0
        }
    )

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
