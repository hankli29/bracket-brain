# use pip install to install public/external libraries on global machine

# must then actually import those libraries into this file to use them
import requests
from dotenv import load_dotenv
import os # os lib is used to access environment variables (API keys)

load_dotenv() # makes everything in the .env file visible to program

# access .env variables (api keys)
odds_key = os.getenv("ODDS_API_KEY")

# put logic of making API call and fetching data all in a method
# allows importing module to control when to make calls, otherwise a call would be made for every single import
def get_data():
    # get() method returns a response object (a package containing data, headers, status code)
    # url must be entered as a string
    response = requests.get(f"https://api.the-odds-api.com/v4/sports/basketball_ncaab/odds?apiKey={odds_key}&regions=us&markets=h2h&oddsFormat=american")
    print(f"Requests remaining: {response.headers['x-requests-remaining']}")
    print(f"API call status code: {response.status_code}\n")

    odds_data = response.json()

    return odds_data

if __name__ == "__main__":
    test_data = get_data()
    print(test_data)