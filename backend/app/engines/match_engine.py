import random

# -------------------------
# UTILIDADES
# -------------------------

def age_modifier(age: int) -> float:
    if age < 23:
        return 1 + (23 - age) * 0.02
    if age > 30:
        return 1 - (age - 30) * 0.03
    return 1.0


def random_factor() -> float:
    return random.uniform(0.9, 1.1)


# -------------------------
# DUELO DELANTERO - PORTERO
# -------------------------

def goal_duel(attacker: dict, goalkeeper: dict, chance_type: str) -> bool:
    attack = (
        attacker["ANOTACION"] * 0.6 +
        attacker["JUGADAS"] * 0.25 +
        attacker["FORMA"] * 0.1 +
        attacker["CONDICION"] * 0.05
    )

    defense = (
        goalkeeper["PORTERIA"] * 0.7 +
        goalkeeper["DEFENSA"] * 0.15 +
        goalkeeper["FORMA"] * 0.1 +
        goalkeeper["CONDICION"] * 0.05
    )

    attack *= age_modifier(attacker["EDAD"])
    defense *= age_modifier(goalkeeper["EDAD"])

    # Modificadores por tipo de ocasión
    if chance_type == "mano_a_mano":
        attack *= 1.10
    elif chance_type == "tiro_lejano":
        attack *= 0.85
    elif chance_type == "penal":
        attack *= 1.25
    elif chance_type == "tiro_libre":
        attack *= (1 + attacker.get("BALON_PARADO", 0) * 0.05)

    result = attack * random_factor() - defense
    return result > 0


# -------------------------
# EVENTOS ESPECIALES
# -------------------------

def special_event(attacker: dict) -> bool:
    if "CABEZAZO" in attacker.get("HABILIDADES_ESPECIALES", []):
        return random.random() < 0.15
    if "TIRO_POTENTE" in attacker.get("HABILIDADES_ESPECIALES", []):
        return random.random() < 0.10
    return False


# -------------------------
# GENERAR OCASIONES
# -------------------------

def generate_chances(team_level: int) -> int:
    base = team_level // 10
    return max(2, min(15, base + random.randint(-1, 2)))


def chance_minute_distribution(chances: int) -> list:
    minutes = sorted(random.sample(range(1, 91), chances))
    return minutes


# -------------------------
# MATCH ENGINE PRINCIPAL
# -------------------------

def play_match(team_a: dict, team_b: dict) -> dict:
    result = {
        "team_a_goals": 0,
        "team_b_goals": 0,
        "events": []
    }

    chances_a = generate_chances(team_a["NIVEL"])
    chances_b = generate_chances(team_b["NIVEL"])

    minutes_a = chance_minute_distribution(chances_a)
    minutes_b = chance_minute_distribution(chances_b)

    for minute in minutes_a:
        attacker = random.choice(team_a["DELANTEROS"])
        goalkeeper = team_b["PORTERO"]

        chance_type = random.choices(
            ["normal", "mano_a_mano", "tiro_lejano", "penal", "tiro_libre"],
            [50, 20, 15, 5, 10]
        )[0]

        if goal_duel(attacker, goalkeeper, chance_type):
            result["team_a_goals"] += 1
            result["events"].append(f"{minute}' GOL Team A ({chance_type})")
        elif special_event(attacker):
            result["events"].append(f"{minute}' Evento especial Team A")

    for minute in minutes_b:
        attacker = random.choice(team_b["DELANTEROS"])
        goalkeeper = team_a["PORTERO"]

        chance_type = random.choices(
            ["normal", "mano_a_mano", "tiro_lejano", "penal", "tiro_libre"],
            [50, 20, 15, 5, 10]
        )[0]

        if goal_duel(attacker, goalkeeper, chance_type):
            result["team_b_goals"] += 1
            result["events"].append(f"{minute}' GOL Team B ({chance_type})")
        elif special_event(attacker):
            result["events"].append(f"{minute}' Evento especial Team B")

    return result
