from datetime import datetime

# -------------------------
# CONSTANTES
# -------------------------

MAX_SKILL = 20
MAX_AGE = 32
MAX_COACH_LEVEL = 5

TRAINABLE_SKILLS = [
    "goalkeeping",
    "defense",
    "playmaking",
    "passing",
    "winger",
    "scoring",
    "set_pieces"
]

# -------------------------
# PARTIDOS NECESARIOS SEGÚN EDAD
# -------------------------

def matches_needed_for_training(age):
    if age <= 18:
        return 3
    elif age <= 20:
        return 4
    elif age <= 22:
        return 5
    elif age <= 24:
        return 6
    elif age <= 26:
        return 7
    elif age <= 28:
        return 9
    elif age <= 30:
        return 12
    elif age <= 32:
        return 15
    else:
        return None  # no entrena


# -------------------------
# ¿QUIÉN ENTRENA QUÉ?
# -------------------------

def can_train(player_position, skill):
    if skill == "goalkeeping":
        return player_position == "GK"
    if skill == "defense":
        return player_position == "DEF"
    if skill == "playmaking":
        return player_position == "MID"
    if skill == "scoring":
        return player_position == "ATT"
    if skill == "winger":
        return player_position in ["MID", "ATT"]
    if skill in ["passing", "set_pieces"]:
        return True
    return False


# -------------------------
# INICIALIZAR PROGRESO
# -------------------------

def init_training_progress(player):
    if "training_progress" not in player:
        player["training_progress"] = {
            skill: 0 for skill in TRAINABLE_SKILLS
        }

    if "coach_bonus_counter" not in player:
        player["coach_bonus_counter"] = {
            skill: 0 for skill in TRAINABLE_SKILLS
        }

    return player


# -------------------------
# ENTRENAMIENTO POR PARTIDO
# -------------------------

def train_player_match(player, skill_focus, coach_level):
    """
    Entrenamiento de UN partido
    """

    player = init_training_progress(player)

    if player["age"] > MAX_AGE:
        return player

    if not can_train(player["position"], skill_focus):
        return player

    if player[skill_focus] >= MAX_SKILL:
        return player

    base_matches = matches_needed_for_training(player["age"])
    if not base_matches:
        return player

    # -------------------------
    # EFECTO ENTRENADOR
    # -------------------------

    coach_level = min(coach_level, MAX_COACH_LEVEL)

    # Reducción de partidos (máx -1)
    effective_matches = max(1, base_matches - (1 if coach_level == 5 else 0))

    # Progreso normal
    player["training_progress"][skill_focus] += 1
    player["coach_bonus_counter"][skill_focus] += 1

    # Subida normal
    if player["training_progress"][skill_focus] >= effective_matches:
        player[skill_focus] += 1
        player["training_progress"][skill_focus] = 0

    # -------------------------
    # BONUS ENTRENADOR NIVEL 5
    # -------------------------

    if coach_level == 5:
        if player["coach_bonus_counter"][skill_focus] >= 5:
            if player[skill_focus] < MAX_SKILL:
                player[skill_focus] += 1
            player["coach_bonus_counter"][skill_focus] = 0

    # Seguridad
    player[skill_focus] = min(player[skill_focus], MAX_SKILL)

    return player


# -------------------------
# MOTOR DE ENTRENAMIENTO
# -------------------------

def training_engine(team, players, skill_focus, matches_played=1):
    """
    Entrena al equipo según los partidos jugados
    """

    if skill_focus not in TRAINABLE_SKILLS:
        raise ValueError("Habilidad no válida")

    coach_level = team.get("coach_level", 1)

    for _ in range(matches_played):
        for player in players:
            train_player_match(player, skill_focus, coach_level)

    return {
        "trained_skill": skill_focus,
        "matches": matches_played,
        "coach_level": coach_level,
        "players": players
    }


# -------------------------
# FIN DE TEMPORADA
# -------------------------

def end_of_season(players):
    """
    Envejece a los jugadores al final del año
    """
    for player in players:
        player["age"] += 1

    return {
        "season_ended": datetime.utcnow().year,
        "players": players
    }
