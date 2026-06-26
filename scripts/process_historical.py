import kagglehub
import pandas as pd
from pathlib import Path

# downloads latest version of march madness data
path = kagglehub.dataset_download("nishaanamin/march-madness-data")

kenpom_bart_df = pd.read_csv(f"{path}/KenPom Barttorvik.csv")

kenpom_bart_df = kenpom_bart_df[["YEAR", "TEAM", "SEED", "KADJ O", "KADJ D", "KADJ EM", "BARTHAG",
                                 "WIN%", "EXP", "TALENT", "ELITE SOS", "KADJ T", "BADJ T", 
                                 "TOV%", "TOV%D", "OREB%", "DREB%", "3PTR", "3PT%"]]
stats_2026_df = kenpom_bart_df[kenpom_bart_df["YEAR"] == 2026].drop("YEAR", axis = 1)

kenpom_bart_df = kenpom_bart_df[kenpom_bart_df["YEAR"] < 2026]

kenpom_bart_df.reset_index(drop=True, inplace=True)
# set multi-index to (YEAR, TEAM) -> can retrieve rows according to specific YEAR and TEAM values
kenpom_bart_df.set_index(["YEAR", "TEAM"], inplace=True)

# only need year, team name, and score from matchups
# YEAR and TEAM to match outcome with corresponding team's stats, score to determine winner
matchups_df = pd.read_csv(f"{path}/Tournament Matchups.csv")[["YEAR", "TEAM", "SCORE"]]
matchups_df = matchups_df[matchups_df["YEAR"] < 2026].reset_index(drop=True)


i = 0
match_stats_df = pd.DataFrame()
data_rows = []

while (i < len(matchups_df)):
    winner = None

    row1 = matchups_df.iloc[i]
    team1 = row1["TEAM"].strip() # remove whitespace as it can cause lookup failure
    score1 = row1["SCORE"]

    row2 = matchups_df.iloc[i + 1]
    team2 = row2["TEAM"].strip()
    score2 = row2["SCORE"]

    year = row1["YEAR"]

    if score1 > score2:
        winner = 0
    else:
        winner = 1
    
    t1_data = kenpom_bart_df.loc[[(year, team1)]]
    t2_data = kenpom_bart_df.loc[[(year, team2)]]

    # rename the columns of each individual data frame to avoid name collisions -> prevent ambiguity
    # multi-indices were originally different -> reset index to have resulting data frame be single row and avoid NaNs
    data_row_v1 = pd.concat([t1_data.add_suffix(" T1").reset_index(drop=True), t2_data.add_suffix(" T2").reset_index(drop=True)], axis = 1)
    data_row_v1["WINNER"] = winner

    # higher seed team is always T1 in raw data -> duplicate rows but swap T1 and T2 labels
    # to prevent model from naively creating correlation between teams being labeled as T1 and winning
    data_row_v2 = pd.concat([t1_data.add_suffix(" T2").reset_index(drop=True), t2_data.add_suffix(" T1").reset_index(drop=True)], axis = 1)
    data_row_v2["WINNER"] = 0 if winner == 1 else 1

    data_rows.append(data_row_v1)
    data_rows.append(data_row_v2)
    
    i += 2

# concatenating vertically keeps each row's row index (all 0s in this case) -> must reset index
match_stats_df = pd.concat(data_rows).reset_index(drop=True)

base_dir = Path(__file__).resolve().parent.parent
# save historical data to a separate csv file
match_stats_df.to_csv(base_dir / "data" / "historical_data.csv", index=False)
stats_2026_df.to_csv(base_dir / "data" / "2026_team_stats.csv", index=False)