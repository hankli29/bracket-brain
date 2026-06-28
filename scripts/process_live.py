from fetch_data import get_data

def find_game(odds_data, team1, team2):
    for game in odds_data:
        home, away = game["home_team"], game["away_team"]

        if {team1, team2} == {home, away}:
            return game
    
    return None


def process_odds(game_data, team1, team2):
    ml_t1, ml_t2 = [], []
    spread_t1, spread_t2 = [], []
    total_ou = []

    if game_data is not None:
        for bookmaker in game_data["bookmakers"]:
            for market in bookmaker["markets"]:
                if market["key"] == "h2h": # h2h == moneyline
                    for outcome in market["outcomes"]:
                        if outcome["name"] == team1:
                            ml_t1.append(outcome["price"])
                        elif outcome["name"] == team2: # explicitly check in case there is a third possible outcome that is neither team
                            ml_t2.append(outcome["price"])

                elif market["key"] == "spreads":
                    for outcome in market["outcomes"]:
                        if outcome["name"] == team1:
                            spread_t1.append(outcome["point"])
                        elif outcome["name"] == team2:
                            spread_t2.append(outcome["point"])

                else: # market == total o/u
                    total_ou.append(market["outcomes"][0]["point"])
    
    return {
        "ML T1": sum(ml_t1) / len(ml_t1) if len(ml_t1) > 0 else float("nan"),
        "SPREAD T1": sum(spread_t1) / len(spread_t1) if len(spread_t1) > 0 else float("nan"),
        "ML T2": sum(ml_t2) / len(ml_t2) if len(ml_t2) > 0 else float("nan"),
        "SPREAD T2": sum(spread_t2) / len(spread_t2) if len(spread_t2) > 0 else float("nan"),
        "TOTAL OU": sum(total_ou) / len(total_ou) if len(total_ou) > 0 else float("nan")
    }