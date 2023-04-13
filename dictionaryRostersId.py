import pandas as pd

rostersHashTable = {}

df = pd.read_csv("./converted_files/rosters.csv")

for index, row in df.iterrows():
    # rostersHashTable.add(
    #     (
    #         "team_name": row["Team"],
    #         "player_id": row["Player_id"],
    #         "year_start": row["Year_start"],
    #         "year_end": row["Year_end"],
    #     ):row["id_roster"]
    # )
    # rostersHashTable.add(
    new_key = (row["Team"], row["Player_id"], row["Year_start"], row["Year_end"])
    new_value = row["id_roster"]
    rostersHashTable[new_key] = new_value

f = open("rostersHashMap.py", "w")
f.write("rostersHashTable = " + str(rostersHashTable))
f.close()
# print(rostersHashTable)
