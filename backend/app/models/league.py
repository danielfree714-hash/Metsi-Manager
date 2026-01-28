from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Liga Metsi")
    season = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    
    current_week = Column(Integer, default=1)
    total_weeks = Column(Integer, default=16)
    
    # Standings (JSON: {team_id: {points, played, wins, ...}})
    standings = Column(JSON, default=dict)
    
    # Schedule (JSON: [[(home_id, away_id), ...], ...])
    schedule = Column(JSON, default=list)
    
    is_active = Column(Boolean, default=True)
    season_ended = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    # Relaciones
    matches = relationship("Match", back_populates="league", cascade="all, delete-orphan")