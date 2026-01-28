import random
from datetime import datetime
from faker import Faker

fake = Faker("es_ES")

# -------------------------
# CONSTANTES DEL JUEGO
# -------------------------

POSITIONS = {
    "GK": 2,
    "DEF": 5,
    "MID": 5,
    "ATT": 4
}

SKILLS = [
    "goalkeeping",
    "defense",
    "playmaking",
    "passing",
    "winger",
    "scoring",
    "set_pieces"
]

TOTAL_PLAYERS = 16
INITIAL_MONEY = 100_000
INITIAL_STADIUM_CAPACITY = 12_000
COACH_LEVEL = 5

AGE_MIN = 17
AGE_MAX = 32


# -------------------------
# UTILIDADES
# -------------------------

def random_skill(min_val=3, max_val=7):
    return random.randint(min_val, max_val)


def generate_player_name():
    return f"{fake.first_name_male()} {fake.last_name()}"


def generate_age():
    return random.randint(AGE_MIN, AGE_MAX)


# -------------------------
# CREAR JUGADOR
# -------------------------

def create_player(team_id, position):
    player = {
        "team_id": team_id,
        "name": generate_player_name(),
        "age": generate_age(),
        "position": position,

        # Skills
        "goalkeeping": random_skill(),
        "defense": random_skill(),
        "playmaking": random_skill(),
        "passing": random_skill(),
        "winger": random_skill(),
        "scoring": random_skill(),
        "set_pieces": random_skill(),

        # Estado
        "stamina": random.randint(5, 8),
        "form": random.randint(5, 8),

        # Progresión
        "seasons_played": 0,
        "training_progress": {s: 0 for s in SKILLS},

        "created_at": datetime.utcnow()
    }

    # Boost por posición
    boosts = {
        "GK": ("goalkeeping", (9, 13)),
        "DEF": ("defense", (8, 12)),
        "MID": ("playmaking", (8, 12)),
        "ATT": ("scoring", (8, 12))
    }

    skill, (a, b) = boosts[position]
    player[skill] = random.randint(a, b)

    return player


# -------------------------
# CREAR EQUIPO
# -------------------------

def create_team(user_id, team_name):
    year = datetime.utcnow().year

    return {
        "user_id": user_id,
        "name": team_name,
        "money": INITIAL_MONEY,
        "stadium_capacity": INITIAL_STADIUM_CAPACITY,
        "fan_mood": 5,
        "coach_level": COACH_LEVEL,
        "current_season": 1,
        "current_year": year,
        "created_at": datetime.utcnow()
    }


# -------------------------
# MOTOR PRINCIPAL
# -------------------------

def team_creation_engine(user_id, team_name):
    team = create_team(user_id, team_name)
    team_id = "TEMP_ID"

    players = []
    for pos, qty in POSITIONS.items():
        for _ in range(qty):
            players.append(create_player(team_id, pos))

    if len(players) != TOTAL_PLAYERS:
        raise ValueError("Error en creación de jugadores")

    return {"team": team, "players": players}
