import pandas as pd
# THE WAY TO IMPORT files from .. or parent directory 
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from player_rating import data_unification
from constants import league_teams_dict

df = None
index = 0
for league, teams in league_teams_dict.items():
    #print(f'LEAGUE {league} :')
    #print()
    for team in teams:
        #print(f'{team}')
        for year in range(2014,2021):
                try:
                    df2 = data_unification(league, team, year, year + 1)
                except ValueError:
                    print("NOT VALID POSITIONS")
                    continue
                except FileNotFoundError:
                    print("NOT FOUND FILE")
                    continue
                except TypeError:
                    print("CLEAN_SHEETS NOT FOUND")
                    continue

                if index == 0:
                    df = df2
                    index = 1
                    #print(df.tail(10))
                    print(len(df))
                else:
                    df = pd.concat([df,df2], ignore_index = True)
                    #print(df.tail(10))
                    print(len(df))
            

#df = data_unification('bundesliga','Bayer Leverkusen', 2014,2015)

#print(df.tail(10))

df.to_csv('utils_for_ml/unified_teams.csv')