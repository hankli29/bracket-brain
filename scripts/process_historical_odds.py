import pandas as pd
import requests
from pathlib import Path
from io import StringIO

def main():
    base_dir = Path(__file__).resolve().parent.parent

    data_rows = []
    for i in range(15):
        start_year = 2007 + i
        if start_year == 2019:
            continue # 19-20 was covid year, no tournament
        elif start_year == 2021:
            # handle table for 21-22 separately as it cannot be downloaded as excel file
            # use User-Agent:Mozilla/5.0 header to make it seem as if request is coming from a web browser/human, not automation script
            url = "https://www.sportsbookreviewsonline.com/scoresoddsarchives/ncaa-basketball-2021-22/"
            headers = {"User-Agent":"Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            tables = pd.read_html(StringIO(response.text), header=0)
            df = tables[0]
        else:
            end_year = (start_year + 1) % 100 # only want last 2 digits

            df = pd.read_excel(base_dir / "data" / "historical_odds" / f"ncaa-basketball-{start_year}-{end_year:02d}.xlsx")
        
        df["YEAR"] = start_year + 1

        data_rows.append(df)


    historical_odds = pd.concat(data_rows).reset_index(drop=True)

    historical_odds.to_csv(base_dir / "data" / "raw_historical_odds.csv", index=False)
    # print(f"Loaded {len(historical_odds)} rows across {historical_odds['YEAR'].nunique()} seasons")
    # print(historical_odds['YEAR'].value_counts().sort_index())

if __name__ == "__main__":
    main()