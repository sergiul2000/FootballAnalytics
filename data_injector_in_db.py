import pandas as pd
import requests

# import sys
# import os.path

# sys.path.append(
#     os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# )

from rostersHashMap import rostersHashTable
from player_name_hashmap import player_name_hashmap


def insert_into_players_defensive():
    iterator = 1
    df = pd.read_csv("./converted_files/players_defensive_stats.csv")
    for index, row in df.iterrows():
        # print(row)
        URL = "http://localhost:8080/football-analytics/playerDefensive"

        obj = {
            "defensive_id": iterator,
            "clearances_per_game": row["clearances_per_game"],
            "dribbled_past_per_game": row["dribbled_past_per_game"],
            "fouls_per_game": row["fouls_per_game"],
            "id_player": row["player_number"],
            "interceptions_per_game": row["interceptions_per_game"],
            "offsides_won_per_game": row["offsides_won_per_game"],
            "outfielder_blocks_per_game": row["outfielder_blocks_per_game"],
            "own_goals": row["own_goals"],
            "player_name": player_name_hashmap[row["player_number"]],
            "tackles_per_game": row["tackles_per_game"],
            "player_name": player_name_hashmap[row["player_number"]],
            "team_name": row["Team"],
            "year_end": row["Year_end"],
            "year_start": row["Year_start"],
            "id_roster": rostersHashTable[
                (row["Team"], row["player_number"], row["Year_start"], row["Year_end"])
            ],
        }
        x = requests.post(URL, json=obj)
        print(x.text)
        iterator += 1
        # if iterator == 1000:
        #     break


def insert_into_players_offensive():
    iterator = 1
    df = pd.read_csv("./converted_files/players_offensive_stats.csv")
    for index, row in df.iterrows():
        # print(row)
        URL = "http://localhost:8080/football-analytics/playerOffensive"

        obj = {
            "offensive_id": iterator,
            "bad_control_per_game": row["bad_control_per_game"],
            "dispossessed_per_game": row["dispossessed_per_game"],
            "dribbles_per_game": row["dribbles_per_game"],
            "fouled_per_game": row["fouled_per_game"],
            "id_player": row["id_player"],
            "offsides_per_game": row["offsides_per_game"],
            "player_name": player_name_hashmap[row["id_player"]],
            "team_name": row["Team"],
            "year_end": row["Year_end"],
            "year_start": row["Year_start"],
            "id_roster": rostersHashTable[
                (row["Team"], row["id_player"], row["Year_start"], row["Year_end"])
            ],
        }
        x = requests.post(URL, json=obj)
        print(x.text)
        iterator += 1


def insert_into_players_summary():
    iterator = 1
    df = pd.read_csv("./converted_files/player_summary_stats.csv")
    for index, row in df.iterrows():
        # print(row)
        URL = "http://localhost:8080/football-analytics/playerSummary"

        obj = {
            "summary_id": iterator,
            "player_name": player_name_hashmap[row["player_number"]],
            "team_name": row["Team"],
            "year_end": row["Year_end"],
            "year_start": row["Year_start"],
            "games": row["games"],
            "start_games": row["start_games"],
            "sub_games": row["sub_games"],
            "mins": row["mins"],
            "goals": row["goals"],
            "assists": row["assists"],
            "mins": row["yellow_cards"],
            "goals": row["red_cards"],
            "assists": row["shots_per_game"],
            "goals": row["pass_success_percentage"],
            "assists": row["aerials_won"],
            "assists": row["man_of_the_match"],
            "assists": row["rating"],
            "id_roster": rostersHashTable[
                (row["Team"], row["player_number"], row["Year_start"], row["Year_end"])
            ],
        }
        x = requests.post(URL, json=obj)
        print(x.text)
        iterator += 1
        break


def insert_into_teams():
    df = pd.read_csv("./converted_files/teams.csv")
    for index, row in df.iterrows():
        # print(row)
        URL = "http://localhost:8080/football-analytics/team"

        obj = {"team_name": row["Team"]}
        x = requests.post(URL, json=obj)
        print(x.text)
        # print(obj)
        # break


def insert_into_leagues():
    df = pd.read_csv("./converted_files/leagues.csv")
    for index, row in df.iterrows():
        # print(row)
        URL = "http://localhost:8080/football-analytics/league"

        obj = {"league_name": row["league_name"]}
        x = requests.post(URL, json=obj)
        print(x.text)


def insert_into_player():
    df = pd.read_csv("./converted_files/players.csv")
    for index, row in df.iterrows():
        # print(row)
        URL = "http://localhost:8080/football-analytics/player"

        obj = {
            "player_id": row["id"],
            "name": row["name"],
            "age": row["age"],
            "position": row["position"],
            "height": row["height"],
            "weight": row["weight"],
        }
        x = requests.post(URL, json=obj)
        print(x.text)


def insert_into_rosters():
    df = pd.read_csv("./converted_files/rosters.csv")
    for index, row in df.iterrows():
        # print(row)
        URL = "http://localhost:8080/football-analytics/rosters"

        obj = {
            "id_roster": row["id_roster"],
            "team_name": row["Team"],
            "player_id": row["Player_id"],
            "year_start": row["Year_start"],
            "year_end": row["Year_end"],
        }
        x = requests.post(URL, json=obj)
        print(x.text)


def main():
    # insert_into_teams()
    # insert_into_leagues()
    # insert_into_player()
    # insert_into_rosters()
    # insert_into_players_defensive()
    # insert_into_players_offensive()
    insert_into_players_summary()


if __name__ == "__main__":
    main()
