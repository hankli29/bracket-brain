import kagglehub
import pandas as pd

# downloads latest version of march madness data
path = kagglehub.dataset_download("nishaanamin/march-madness-data")

# print("Path to dataset files:", path)

kenpom_bart_df = pd.read_csv(f"{path}/KenPom Barttorvik.csv")
# print(kenpom_bart_df.head()) # prints the first 5 rows of data from the  

# indexing into a data frame returns a sub-table/sub-data frame
# single key/column for a series, list of keys for a data frame
# only want to focus on these select data columns
kenpom_bart_df = kenpom_bart_df[["YEAR", "TEAM", "SEED", "KADJ O", "KADJ D", "KADJ EM", "BADJ O", "BADJ D", "BADJ EM", "BARTHAG", "WIN%", "EXP", "TALENT", "ELITE SOS"]]
stats_2026_df = kenpom_bart_df[kenpom_bart_df["YEAR"] == 2026].drop("YEAR", axis = 1)

# kenpom_bart_df["YEAR"] < 2026 creates a boolean mask (true for rows where condition is true, false otherwise)
# kenpom_bart_df[<boolean mask>] returns data frame only containing "true" rows
kenpom_bart_df = kenpom_bart_df[kenpom_bart_df["YEAR"] < 2026]
# after removing 2026 data, row index will no longer start from 0
# must reset index, use drop arg to get rid of old index col, inplace to modify df in place
kenpom_bart_df.reset_index(drop=True, inplace=True)
# set multi-index to (YEAR, TEAM) -> can retrieve rows according to specific YEAR and TEAM values
kenpom_bart_df.set_index(["YEAR", "TEAM"], inplace=True)

# print(kenpom_bart_df.head())

# only need year, team name, and score from matchups
# YEAR and TEAM to match outcome with corresponding team's stats, score to determine winner
matchups_df = pd.read_csv(f"{path}/Tournament Matchups.csv")[["YEAR", "TEAM", "SCORE"]]
matchups_df = matchups_df[matchups_df["YEAR"] < 2026].reset_index(drop=True)


i = 0
# create empty df with specified columns
match_stats_df = pd.DataFrame()
data_rows = []
while (i < len(matchups_df)): # len(df) returns num ROWS
    winner = None

    # indexing with single braces returns series, indices are column names
    row1 = matchups_df.iloc[i]
    team1 = row1["TEAM"].strip() # access values in row series using col name, also remove whitespace as it can cause lookup failure
    score1 = row1["SCORE"]

    row2 = matchups_df.iloc[i + 1]
    team2 = row2["TEAM"].strip()
    score2 = row2["SCORE"]

    year = row1["YEAR"]

    # the winner should be stored as a number: the model learns from numbers, so team name as text wouldn't be helpful
    if score1 > score2:
        winner = 0
    else:
        winner = 1
    
    # indexing with double braces returns a data frame, NOT a series
    t1_data = kenpom_bart_df.loc[[(year, team1)]]
    t2_data = kenpom_bart_df.loc[[(year, team2)]]

    # rename the columns of each individual data frame to avoid name collisions -> prevent ambiguity
    # multi-indices were originally different -> reset index to have resulting data frame be single row and avoid NaNs
    data_row = pd.concat([t1_data.add_suffix(" T1").reset_index(drop=True), t2_data.add_suffix(" T2").reset_index(drop=True)], axis = 1)
    data_row["WINNER"] = winner # create new column with winner (crete using key, value pair)

    data_rows.append(data_row)
    
    i += 2

# concatenating vertically keeps each row's row index (all 0s in this case) -> must reset index
match_stats_df = pd.concat(data_rows).reset_index(drop=True)


# save historical data to a separate csv file so data can be imported and used in other files
# by fault pandas saves row indices as an extra column -> unnecessary and model will treat as a feature (unwanted)
match_stats_df.to_csv("../historical_data.csv", index=False)
stats_2026_df.to_csv("../2026_team_stats.csv", index=False)