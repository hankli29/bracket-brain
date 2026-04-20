from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb
import pandas as pd
import pickle
import mlflow
import mlflow.xgboost


historical_data = pd.read_csv("/Users/hankli/Projects/bracket-brain/historical_data.csv")

# drop method returns data frame excluding specified rows/cols (axis defaults to 0 (rows))
historical_stats = historical_data.drop("WINNER", axis=1)
historical_outcomes = historical_data["WINNER"]

# we need to separate data into separate training and testing sets to avoid overfitting
# train using training set, check accuracy with testing set
x_train, x_test, y_train, y_test = train_test_split(historical_stats, historical_outcomes, test_size = 0.2)

# set training parameters for xgboost
params = {
    "n_estimators": 100,
    "max_depth": 4,
    "learning_rate": 0.1,
}

mlflow.set_experiment("bracketbrain")

with mlflow.start_run():
    # creates the model with specified training parameters
    # "**params" unpacks the entire params dict
    model = xgb.XGBClassifier(**params)

    # train the model using training data -> xgboost handles training
    model.fit(x_train, y_train)

    # have the model make predictions on the test data
    predictions = model.predict(x_test)
    # accuracy_score calculates the accuracy of the model's predictions
    accuracy = accuracy_score(y_test, predictions)

    mlflow.log_params(params)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.xgboost.log_model(model, name="model")

    print(f"Accuracy: {accuracy:.4f}")

# use pickle to serialize the model and store it in a file
# model can then be imported and used in other files without recreating/retraining
with open("/Users/hankli/Projects/bracket-brain/trained_model.pkl", "wb") as file:
    pickle.dump(model, file)