from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb
import pandas as pd
import pickle
import mlflow
import mlflow.xgboost
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent

# historical_data = pd.read_csv(base_dir / "data" / "historical_data.csv")
historical_data = pd.read_csv(base_dir / "data" / "final_training_data.csv")

# "YEAR", "TEAM", "SEED", "KADJ O", "KADJ D", "KADJ EM", "BARTHAG", "WIN%", "EXP", "TALENT", "ELITE SOS", "KADJ T", "BADJ T", 
# "TOV%", "TOV%D", "OREB%", "DREB%", "3PTR", "3PT%"

historical_stats = historical_data.drop(["TEAM T1", "TEAM T2", "WINNER", "YEAR", "DATE"], axis=1)
# historical_stats = historical_data.drop(["TEAM T1", "TEAM T2", "WINNER"], axis=1)
historical_outcomes = historical_data["WINNER"]

params = {
    "n_estimators": 100,
    "max_depth": 4,
    "learning_rate": 0.05,
}

mlflow.set_experiment("madnessmapper")

x_train, x_test, y_train, y_test = train_test_split(historical_stats, historical_outcomes, test_size = 0.2, random_state=123)
with mlflow.start_run():
    model = xgb.XGBClassifier(**params, random_state=123)

    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    mlflow.log_params(params)
    mlflow.log_param("features", ", ".join(historical_stats.columns))
    mlflow.log_metric("accuracy", accuracy)
    mlflow.xgboost.log_model(model, name="model")

    # mlflow.xgboost.auto_log() automatically logs all these metrics, can replace above

    print(f"Accuracy: {accuracy:.4f}")

# use pickle to serialize the model and store it in a file
# model can then be imported and used in other files without recreating/retraining
with open(base_dir / "models" / "trained_model.pkl", "wb") as file:
    pickle.dump(model, file)