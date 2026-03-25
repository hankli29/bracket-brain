import kagglehub
import pandas as pd

# downloads latest version of march madness data
path = kagglehub.dataset_download("nishaanamin/march-madness-data")

print("Path to dataset files:", path)

kenpom_bart_df = pd.read_csv(f"{path}/KenPom Barttorvik.csv")
# print(kenpom_bart_df.head()) # prints the first 5 rows of data from the dataframe

# indexing into a dataframe returns a sub-table/sub-dataframe
# single key/column for a series, list of keys for a dataframe
# only want to focus on these select data columns
kenpom_bart_df = kenpom_bart_df[["YEAR", "TEAM", "SEED", "ROUND", "KADJ O", "KADJ D", "KADJ EM", "BADJ EM", "BADJ O", "BADJ D", "BARTHAG", "WIN%", "EXP", "TALENT", "ELITE SOS"]]
# data for current year (2026) has every team ROUND stat = 0, this will skew data

# kenpom_bart_df["ROUND"] > 0 creates a boolean mask (true for rows where condition is true, false otherwise)
# kenpom_bart_df[<boolean mask>] returns dataframe only containing "true" rows
kenpom_bart_df = kenpom_bart_df[kenpom_bart_df["ROUND"] > 0]
# after removing 2026 data, row index will no longer start from 0
# must reset index, use drop arg to get rid of old index col
kenpom_bart_df = kenpom_bart_df.reset_index(drop=True)

# print(kenpom_bart_df.head())

# only need year, team name, and score from matchups
# YEAR and TEAM to match outcome with corresponding team's stats, score to determine winner
matchups_df = pd.read_csv(f"{path}/Tournament Matchups.csv")[["YEAR", "TEAM", "SCORE"]]
matchups_df = matchups_df[matchups_df["YEAR"] < 2026].reset_index(drop=True)
print(matchups_df.head())

i = 0
while (i < len(matchups_df)): # len(df) returns num ROWS
    winner = None

    row1 = matchups_df.iloc[i]
    team1 = row1["TEAM"] # access values in row series using col name
    score1 = row1["SCORE"]

    row2 = matchups_df.iloc[i + 1]
    team2 = row2["TEAM"]
    score2 = row2["SCORE"]

    year = row1["YEAR"]

    if score1 > score2:
        winner = team1
    else:
        winner = team2
    
    
    

    i += 2