# this module should receive data as a paramter
# it should NOT do the calling itself (isolate functionality)


def process_odds(odds_data):
    processed_data = []

    # we want to loop through all the data and extract 3 things
    # team names, average odds, and game commencement time

    for game in odds_data:
        game_info = {}
        game_info["home_team"] = game["home_team"]
        game_info["away_team"] = game["away_team"]
        game_info["start_time"] = game["commence_time"]

        home_odds = 0
        away_odds = 0

        books = game["bookmakers"]
        for book in books:
            name1 = book["markets"][0]["outcomes"][0]["name"]
            odds1 = book["markets"][0]["outcomes"][0]["price"]
            odds2 = book["markets"][0]["outcomes"][1]["price"]

            # odds are ordered alphabetically, not according to home/away
            # must check which team each odds is for
            if name1 == game["home_team"]:
                home_odds += odds1
                away_odds += odds2
            else:
                home_odds += odds2
                away_odds += odds1
        
        # ensure that books is not empty -> only calculate average if not empty
        if len(books) > 0:
            # average odds to find the CONSENSUS LINE (because every book has their own odds)
            game_info["home_odds"] = int(home_odds / len(books))
            game_info["away_odds"] = int(away_odds / len(books))
        else:
            game_info["home_odds"] = None
            game_info["away_odds"] = None

        # add dictionary to list of all game info
        processed_data.append(game_info)

    return processed_data

if __name__ == "__main__":
    from fetch_data import get_data

    odds_data = get_data()
    print(process_odds(odds_data))