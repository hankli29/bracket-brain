import pickle
import pandas as pd

with open("../trained_model.pkl", "rb") as file:
    model = pickle.load(file)

current_data = pd.read_csv("../2026_team_stats.csv")

def predict_winner(team1, team2):
    t1_data = current_data[current_data["TEAM"] == team1]
    t2_data = current_data[current_data["TEAM"] == team2]

    prediction_data = pd.concat([t1_data.add_suffix(" T1").reset_index(drop=True), t2_data.add_suffix(" T2").reset_index(drop=True)], axis = 1).drop(["TEAM T1", "TEAM T2"], axis=1)
    prediction = model.predict(prediction_data)
    prob = model.predict_proba(prediction_data)
    # return the winner and the confidence level
    if prediction[0] == 0:
        return team1, prob[0][0]
    else:
        return team2, prob[0][1]