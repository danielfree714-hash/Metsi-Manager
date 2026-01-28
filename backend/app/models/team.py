from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)

    # Relación con usuario
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    user = relationship("User", back_populates="team")

    # Identidad
    name = Column(String(100), unique=True, nullable=False)

    # Economía
    money = Column(Integer, default=100_000)

    # Infraestructura
    stadium_capacity = Column(Integer, default=12_000)
    fan_mood = Column(Integer, default=5)

    # Progreso
    level = Column(Integer, default=1)
    coach_level = Column(Integer, default=5)

    # Temporadas
    current_season = Column(Integer, default=1)
    founded_year = Column(Integer)
    current_year = Column(Integer)

    # Relaciones
    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")
    home_matches = relationship("Match", foreign_keys="[Match.home_team_id]")
    away_matches = relationship("Match", foreign_keys="[Match.away_team_id]")

    league_id = Column(Integer, ForeignKey("leagues.id"))
    league = relationship("League", back_populates="teams")

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
