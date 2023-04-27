import pandas as pd

hash_table = {}

df = pd.read_csv("./converted_files/players.csv")

for index, row in df.iterrows():
    new_key = row["id"]
    new_value = row["name"]
    hash_table[new_key] = new_value

# print(hash_table[8040])
f = open("player_name_hashmap.py", "w", encoding="utf-8")
f.write("player_name_hashmap = " + str(hash_table))
f.close()
# print(rostersHashTable)
