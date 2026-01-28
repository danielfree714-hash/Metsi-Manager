TICKET_PRICE = 12
BASE_ATTENDANCE_RATE = 0.65
WIN_BONUS = 20_000
DRAW_BONUS = 8_000
STADIUM_MAINTENANCE_PERCENT = 0.03


def calculate_attendance(capacity, mood):
    return int(capacity * BASE_ATTENDANCE_RATE * (mood / 10))


def season_economy_engine(team, home_results):
    income = 0
    bonus = 0

    for r in home_results:
        income += calculate_attendance(team["stadium_capacity"], team["fan_mood"]) * TICKET_PRICE

        if r == "win":
            bonus += WIN_BONUS
            team["fan_mood"] = min(10, team["fan_mood"] + 1)
        elif r == "draw":
            bonus += DRAW_BONUS
        else:
            team["fan_mood"] = max(1, team["fan_mood"] - 1)

    maintenance = int(team["money"] * STADIUM_MAINTENANCE_PERCENT)
    net = income + bonus - maintenance
    team["money"] += net

    return net
