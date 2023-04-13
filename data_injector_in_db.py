import pandas as pd
import requests
import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from rostersHashMap import rostersHashTable

# rostersHashTable = {}
df = pd.read_csv("./converted_files/players_defensive_stats.csv")
for index, row in df.iterrows():
    # print(row)
    URL = "http://localhost:8080/football-analytics/playerDefensive"
    print(
        rostersHashTable[
            (row["Team"], row["player_number"], row["Year_start"], row["Year_end"])
        ]
    )

    # print((row["Team"], row["player_number"], row["Year_start"], row["Year_end"]))
    # break
    # print(rostersHashTable[("Arsenal", 8040, 2009, 2010)])
    # print(("Arsenal", 8040, 2009, 2010))

    # myobj = {
    #     "clearances_per_game": row["clearances_per_game"],
    #     "dribbled_past_per_game": row["dribbled_past_per_game"],
    #     "fouls_per_game": row["fouls_per_game"],
    #     "interceptions_per_game": row["interceptions_per_game"],
    #     "offsides_won_per_game": row["offsides_won_per_game"],
    #     "outfielder_blocks_per_game": row["outfielder_blocks_per_game"],
    #     "own_goals": row["own_goals"],
    #     "player_number": row["player_number"],
    #     "tackles_per_game": row["tackles_per_game"],
    #     "Team": row["Team"],
    #     "Year_end": row["Year_end"],
    #     "Year_start": row["Year_start"],
    #     "rosters_FK_id": rostersHashTable[
    #         (row["Team"], row["player_number"], row["Year_start"], row["Year_end"])
    #     ],
    # }
    # x = requests.post(URL, json=myobj)
    # print(x.text)
    # break

    # request =
