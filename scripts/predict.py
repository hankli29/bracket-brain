import pickle
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent

with open(base_dir / "models" / "trained_model.pkl", "rb") as file:
    model = pickle.load(file)

current_data = pd.read_csv(base_dir / "data" / "2026_team_stats.csv")

def predict_winner(team1, team2):
    t1_data = current_data[current_data["TEAM"] == team1]
    t2_data = current_data[current_data["TEAM"] == team2]

    prediction_data = pd.concat([t1_data.add_suffix(" T1").reset_index(drop=True), t2_data.add_suffix(" T2").reset_index(drop=True)], axis = 1).drop(["TEAM T1", "TEAM T2"], axis=1)
    probabilities = model.predict_proba(prediction_data)[0]
    # return winner and the confidence level
    if probabilities[0] > probabilities[1]:
        return team1, float(probabilities[0])
    else:
        return team2, float(probabilities[1])