import pandas as pd

rostersHashTable = {}

df = pd.read_csv("./converted_files/rosters.csv")

for index, row in df.iterrows():
    new_key = (row["Team"], row["Player_id"], row["Year_start"], row["Year_end"])
    new_value = row["id_roster"]
    rostersHashTable[new_key] = new_value

f = open("rostersHashMap.py", "w")
f.write("rostersHashTable = " + str(rostersHashTable))
f.close()
# print(rostersHashTable)
