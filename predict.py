import pickle
import pandas as pd

with open("/Users/hankli/bracket-brain/trained_model.pkl", "rb") as file:
    model = pickle.load(file)

current_data = pd.read_csv("/Users/hankli/bracket-brain/2026_team_stats.csv")

def predict_winner(team1, team2):
    t1_data = current_data[current_data["TEAM"] == team1]
    t2_data = current_data[current_data["TEAM"] == team2]

    prediction_data = pd.concat([t1_data.add_suffix(" T1").reset_index(drop=True), t2_data.add_suffix(" T2").reset_index(drop=True)], axis = 1).drop(["TEAM T1", "TEAM T2"], axis=1)
    prediction = model.predict(prediction_data)
    if prediction[0] == 0:
        return team1
    else:
        return team2

# print(predict_winner("Saint Mary's", "Texas A&M"))