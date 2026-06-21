import streamlit as st
import pandas as pd
import pickle
from pathlib import Path
from predict import predict_winner
from dotenv import load_dotenv
import os
from google import genai

base_dir = Path(__file__).resolve().parent.parent


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

@st.cache_resource
def get_gemini_client(key):
   return genai.Client(api_key=key)



load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
client = get_gemini_client(gemini_key)

st.title("BracketBrain")
st.set_page_config(page_title="BracketBrain", page_icon=f"{base_dir}/pictures/favicon.png")

# if st.context.theme.type == "light":
   # st.logo(base_dir / "pictures" / "light_logo.png", size="large")
# else:
   # st.logo(base_dir / "pictures" / "dark_logo.png", size="large")

st.logo(base_dir / "pictures" / "test.png", size="large")
st.html("""
<style>
img[alt=Logo] {
    height: 5em;
}
</style>
""")

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
      loser = team2 if winner == team1 else team1
      prob *= 100
      article = article_for_percent(prob)
      st.write(f"Prediction: {winner} wins with {article} :green-background[{prob:.2f}%] likelihood.")


      t1_data = team_stats[team_stats["TEAM"] == team1]
      t2_data = team_stats[team_stats["TEAM"] == team2]

      try:
         response = client.models.generate_content_stream(
            model="gemini-3.1-flash-lite",
            contents=f"""A separate ML model predicted {winner} to beat {loser} with {prob:.2f}% confidence.
            {winner}'s 2026 stats: {t1_data}
            {loser}'s 2026 stats: {t2_data}

            Stats legend: SEED = regional tournament seed. KADJ O/KADJ D = KenPom adjusted offensive/defensive efficiency. BADJ O/BADJ D = Bart Torvik versions.
            BARTHAG = power rating (higher = stronger). WIN% = season win rate. EXP = roster experience. TALENT = recruiting talent rating.
            ELITE SOS = strength of schedule.

            Write a 3-4 sentence analysis supporting and explaining why this prediction is plausible based on the stats.

            Constraints:
            -Audience: knowledgeable basketball fan.
            -Tone: analytical, plain language, no hype.
            -Plain prose, no bullet points, no headers, no emojis
            -Elaborate significance of key indicating/decision-maker metrics
            -Do not endorse, second-guess, or alter the prediction
            -Do not reference any actual game results, past or future. Treat this as a hypothetical matchup.
            -Format percentage stats as percents, integers without decimals, round other stats to 2 decimal places.
            """
         )

         st.write_stream(chunk.text for chunk in response)
      except Exception as e:
         st.info("Analysis unavailable at this time. Try again later.")
