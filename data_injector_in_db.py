import pandas as pd
import requests

# import sys
# import os.path

# sys.path.append(
#     os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# )

from rostersHashMap import rostersHashTable

# rostersHashTable = {}
iterator = 1
df = pd.read_csv("./converted_files/players_defensive_stats.csv")
for index, row in df.iterrows():
    # print(row)
    URL = "http://localhost:8080/football-analytics/playerDefensive"
    # print(
    #     rostersHashTable[
    #         (row["Team"], row["player_number"], row["Year_start"], row["Year_end"])
    #     ]
    # )

    myobj = {
        "defensive_id": iterator,
        "clearances_per_game": row["clearances_per_game"],
        "dribbled_past_per_game": row["dribbled_past_per_game"],
        "fouls_per_game": row["fouls_per_game"],
        "id_player": row["player_number"],
        "interceptions_per_game": row["interceptions_per_game"],
        "offsides_won_per_game": row["offsides_won_per_game"],
        "outfielder_blocks_per_game": row["outfielder_blocks_per_game"],
        "own_goals": row["own_goals"],
        "tackles_per_game": row["tackles_per_game"],
        "team_name": row["Team"],
        "year_end": row["Year_end"],
        "year_start": row["Year_start"],
        "id_roster": rostersHashTable[
            (row["Team"], row["player_number"], row["Year_start"], row["Year_end"])
        ],
    }
    x = requests.post(URL, json=myobj)
    print(x.text)
    iterator += 1
    # if iterator == 100:
    #     break

    # request =
