import requests
from dotenv import load_dotenv
import os # os lib is used to access environment variables

load_dotenv() # makes everything in the .env file visible to program
odds_key = os.getenv("ODDS_API_KEY")

def get_data():

    # get() method returns a response object (containing data, headers, status code)
    response = requests.get(f"https://api.the-odds-api.com/v4/sports/basketball_ncaab/odds?apiKey={odds_key}&regions=us&markets=h2h,spreads,totals&oddsFormat=american")
    response.raise_for_status()
    # print(f"Requests remaining: {response.headers['x-requests-remaining']}")
    # print(f"API call status code: {response.status_code}\n")

    odds_data = response.json()

    return odds_data

if __name__ == "__main__":
    test_data = get_data()
    print(test_data)