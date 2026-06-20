import streamlit as st
import pandas as pd
import pickle
from pathlib import Path
from predict import predict_winner

st.title("BracketBrain")

base_dir = Path(__file__).resolve().parent.parent
st.logo(base_dir / "logo.png", size="large")
st.html("""
<style>
img[alt=Logo] {
    height: 5em;
}
</style>
""")

def article_for_percent(percent):
   beginning = str(int(percent))

   if (beginning.startswith("8")) or (beginning in {"11", "18"}):
      return "an"
   else:
      return "a"

# st.cache_resource stores return value in cache to prevent expensive repeated execution for reruns
@st.cache_resource
def load_model():
   with open(base_dir / "models" / "trained_model.pkl", "rb") as fp:
      return pickle.load(fp)

@st.cache_data
def load_team_stats():
   with open(base_dir / "data" / "2026_team_stats.csv", "r") as fp:
      return pd.read_csv(fp)



model = load_model()
team_stats = load_team_stats()
teams = team_stats["TEAM"]

team1 = st.selectbox("Select team 1", teams)
team2 = st.selectbox("Select team 2", teams)

if st.button("Predict Winner"):
   if team1 == team2:
      st.error("Please select two different teams", icon="❌")
   else:
      winner, prob = predict_winner(team1, team2)
      prob *= 100
      article = article_for_percent(prob)
      st.write(f"Prediction: {winner} wins with {article} :green-background[{prob:.2f}%] likelihood.")
