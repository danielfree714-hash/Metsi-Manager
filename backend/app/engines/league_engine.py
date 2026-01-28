import random
from datetime import datetime

from match_engine import play_match
from training_engine import training_engine

# -------------------------
# CONFIGURACIÓN DE LIGA V1
# -------------------------

TEAMS_IN_LEAGUE = 8
LEAGUE_WEEKS = 16
LEAGUE_MATCH_WEEKS = 14
FRIENDLY_WEEKS = [15, 16]

POINTS_WIN = 3
POINTS_DRAW = 1
POINTS_LOSS = 0


# -------------------------
# CREAR LIGA
# -------------------------

def create_league(teams):
    """
    teams: dict
    {
        team_id: {
            "team": {...},
            "players": [...]
        }
    }
    """

    if len(teams) != TEAMS_IN_LEAGUE:
        raise ValueError("La liga V1 requiere exactamente 8 equipos")

    standings = {
        team_id: {
            "points": 0,
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0
        }
        for team_id in teams.keys()
    }

    schedule = generate_round_robin_schedule(list(teams.keys()))

    return {
        "teams": teams,
        "standings": standings,
        "schedule": schedule,
        "current_week": 1,
        "created_at": datetime.utcnow()
    }


# -------------------------
# CALENDARIO IDA Y VUELTA
# -------------------------

def generate_round_robin_schedule(team_ids):
    """
    Genera 14 fechas (ida y vuelta) para 8 equipos
    """
    teams = team_ids[:]
    random.shuffle(teams)

    rounds = []
    n = len(teams)

    for i in range(n - 1):
        round_matches = []
        for j in range(n // 2):
            home = teams[j]
            away = teams[n - 1 - j]
            round_matches.append((home, away))
        rounds.append(round_matches)
        teams = [teams[0]] + teams[-1:] + teams[1:-1]

    # vuelta
    return rounds + [(away, home) for round in rounds for (home, away) in round]


# -------------------------
# JUGAR UNA SEMANA
# -------------------------

def play_week(league, training_focus):
    week = league["current_week"]

    print(f"\n📅 Semana {week}")

    if week in FRIENDLY_WEEKS:
        play_friendly_week(league["teams"], training_focus)
        league["current_week"] += 1
        return

    match_day = league["schedule"][week - 1]

    for home_id, away_id in match_day:
        home_team = league["teams"][home_id]
        away_team = league["teams"][away_id]

        result = play_match(
            {"name": home_team["team"]["name"], "players": home_team["players"]},
            {"name": away_team["team"]["name"], "players": away_team["players"]}
        )

        update_standings(
            league["standings"],
            home_id,
            away_id,
            result
        )

        # Entrenamiento cuenta
        training_engine(home_team["team"], home_team["players"], training_focus)
        training_engine(away_team["team"], away_team["players"], training_focus)

    league["current_week"] += 1


# -------------------------
# ACTUALIZAR TABLA
# -------------------------

def update_standings(standings, home_id, away_id, match):
    h = standings[home_id]
    a = standings[away_id]

    hg = match["home_goals"]
    ag = match["away_goals"]

    h["played"] += 1
    a["played"] += 1

    h["goals_for"] += hg
    h["goals_against"] += ag
    a["goals_for"] += ag
    a["goals_against"] += hg

    if hg > ag:
        h["wins"] += 1
        h["points"] += POINTS_WIN
        a["losses"] += 1
    elif ag > hg:
        a["wins"] += 1
        a["points"] += POINTS_WIN
        h["losses"] += 1
    else:
        h["draws"] += 1
        a["draws"] += 1
        h["points"] += POINTS_DRAW
        a["points"] += POINTS_DRAW


# -------------------------
# AMISTOSOS AUTOMÁTICOS
# -------------------------

def play_friendly_week(teams, training_focus):
    print("🤝 Semana de amistosos automáticos")

    team_ids = list(teams.keys())
    random.shuffle(team_ids)

    for i in range(0, len(team_ids), 2):
        team_a = teams[team_ids[i]]
        team_b = teams[team_ids[i + 1]]

        play_match(
            {"name": team_a["team"]["name"], "players": team_a["players"]},
            {"name": team_b["team"]["name"], "players": team_b["players"]}
        )

        training_engine(team_a["team"], team_a["players"], training_focus)
        training_engine(team_b["team"], team_b["players"], training_focus)


# -------------------------
# TEMPORADA COMPLETA
# -------------------------

def play_full_season(league, training_focus):
    while league["current_week"] <= LEAGUE_WEEKS:
        play_week(league, training_focus)

    return league
