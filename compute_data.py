import pandas as pd
import math
df = pd.read_csv("dataframes/player_team_stats/la liga/season_2014_2015/Real Madrid_la liga_players_stats_in_season_2014_2015.csv")
print(df.head(5))

df = pd.read_csv("dataframes/league_table/bundesliga/bundesliga_league_table_in_season_2014_2015.csv")
print(df.head(5))

num=1.5
factorial=1

if num < 0:
   print("Sorry, factorial does not exist for negative numbers")
elif num == 0:
   print("The factorial of 0 is 1")
else:
   #for i in range(1,num + 1):
   #    factorial = factorial*i
#print("The factorial of",num,"is",factorial)
    factorial = math.gamma(1.5)
    print(f"factorial of number {num} is {round(factorial,2)} " )

df = pd.read_csv("dataframes/league_table/bundesliga/bundesliga_league_table_in_season_2014_2015.loc[:,"G"])

#print(
#GS = (80-0,5) / (0,89)
#print(GS)
    #adas#