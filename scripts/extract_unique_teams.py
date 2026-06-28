import pandas as pd
from pathlib import Path

def main():
    base_dir = Path(__file__).resolve().parent.parent

    odds_df = pd.read_csv(base_dir / "data" / "cleaned_historical_odds.csv")
    stats_df = pd.read_csv(base_dir / "data" / "historical_data.csv")

    all_teams = sorted(odds_df["TEAM T1"].unique())
    tournament_teams = sorted(stats_df["TEAM T1"].unique())

    with open(base_dir / "data" / "all_teams.txt", "w") as fp:
        for team in all_teams:
            fp.write(f"{team}\n")
    
    with open(base_dir / "data" / "tournament_teams.txt", "w") as fp:
        for team in tournament_teams:
            fp.write(f"{team}\n")

if __name__ == "__main__":
    main()