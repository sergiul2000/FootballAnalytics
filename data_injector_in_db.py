import pandas as pd
import requests

# import sys
# import os.path

# sys.path.append(
#     os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# )

from rostersHashMap import rostersHashTable
from player_name_hashmap import player_name_hashmap


def insert_into_league_table():
    iterator = 1
    df = pd.read_csv("./converted_files/league_table.csv")
    for index, row in df.iterrows():
        # print(row)
        URL = "http://localhost:8080/football-analytics/leagueTable"
        # print(row)
        # break
        obj = {
            "league_table_id": iterator,
            "league_name": row["League"],
            "team_name": row["Team"],
            "year_end": row["Year_end"],
            "year_start": row["Year_start"],
            "matches": row["M"],
            "wins": row["W"],
            "draws": row["D"],
            "loses": row["L"],
            "goals": row["G"],
            "goalsAgainst": row["GA"],
            "pts": row["PTS"],
            "xGoals": row["xG"],
            "npxGoals": row["NPxG"],
            "xGoalsAgainst": row["xGA"],
            "npxGoalsAgainst": row["NPxGA"],
            "npxGoalsDifference": row["NPxGD"],
            "ppda": row["PPDA"],
            "oppda": row["OPPDA"],
            "dc": row["DC"],
            "odc": row["ODC"],
            "xgoals": row["xG"],
            "xgoalsAgainst": row["xGA"],
        }
        x = requests.post(URL, json=obj)
        print(x.text)
        iterator += 1
        # break


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
        # break


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
            "id_player": row["player_number"],
            "games": row["games"],
            "start_games": row["start_games"],
            "sub_games": row["sub_games"],
            "mins": row["mins"],
            "goals": row["goals"],
            "assists": row["assists"],
            "yellow_cards": row["yellow_cards"],
            "red_cards": row["red_cards"],
            "shots_per_game": row["shots_per_game"],
            "pass_success_percentage": row["pass_success_percentage"],
            "aerials_won": row["aerials_won"],
            "man_of_the_match": row["man_of_the_match"],
            "rating": row["rating"],
            "id_roster": rostersHashTable[
                (row["Team"], row["player_number"], row["Year_start"], row["Year_end"])
            ],
        }
        x = requests.post(URL, json=obj)
        print(x.text)
        iterator += 1
        # break


def insert_into_players_passing():
    iterator = 1
    df = pd.read_csv("./converted_files/players_passing_stats.csv")
    for index, row in df.iterrows():
        # print(row)
        URL = "http://localhost:8080/football-analytics/playerPassing"

        obj = {
            "passing_id": iterator,
            "player_name": player_name_hashmap[row["player_number"]],
            "team_name": row["Team"],
            "id_player": row["player_number"],
            "year_end": row["Year_end"],
            "year_start": row["Year_start"],
            "key_passes_per_game": row["key_passes_per_game"],
            "passes_per_game": row["passes_per_game"],
            "crosses_per_game": row["crosses_per_game"],
            "long_ball_per_game": row["long_ball_per_game"],
            "through_balls_per_game": row["through_balls_per_game"],
            "id_roster": rostersHashTable[
                (row["Team"], row["player_number"], row["Year_start"], row["Year_end"])
            ],
        }
        x = requests.post(URL, json=obj)
        print(x.text)
        iterator += 1
        # break


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
            "league_name": row["League"],
        }
        x = requests.post(URL, json=obj)
        print(x.text)


def insert_into_simple_pythagorean():
    df = pd.read_csv("./converted_files/simple_pythagorean.csv")
    iterator = 1
    for index, row in df.iterrows():
        # print(row)
        URL = "http://localhost:8080/football-analytics/simplePythagorean"

        obj = {
            "simple_pythagorean_id": iterator,
            "league_name": row["League"],
            "team_name": row["Team"],
            "year_end": row["Year_end"],
            "year_start": row["Year_start"],
            "matches": row["Matches"],
            "wins": row["Wins"],
            "draws": row["Draws"],
            "loses": row["Loses"],
            "goals_scored": row["GoalsScored"],
            "goals_received": row["GoalsReceived"],
            "pts": row["Points"],
            "estimated_points_simple_pythagorean": row["Estimated_Points_Simple"],
            "delta_points_simple_pythagorean": row["Delta_Points_Simple"],
        }
        x = requests.post(URL, json=obj)
        print(x.text)
        iterator += 1


def insert_into_extended_pythagorean():
    df = pd.read_csv("./converted_files/extended_pythagorean.csv")
    iterator = 1
    for index, row in df.iterrows():
        # print(row)
        URL = "http://localhost:8080/football-analytics/extendedPythagorean"

        obj = {
            "extended_pythagorean_id": iterator,
            "league_name": row["League"],
            "team_name": row["Team"],
            "year_end": row["Year_end"],
            "year_start": row["Year_start"],
            "matches": row["Matches"],
            "wins": row["Wins"],
            "draws": row["Draws"],
            "loses": row["Loses"],
            "goals_scored": row["GoalsScored"],
            "goals_received": row["GoalsReceived"],
            "pts": row["Points"],
            "estimated_Wins": row["Estimated_Wins"],
            "estimated_Draws": row["Estimated_Draws"],
            "estimated_Loses": row["Estimated_Loses"],
            "estimated_Points_Extended": row["Estimated_Points_Extended"],
            "delta_Points_Extended": row["Delta_Points_Extended"],
        }
        x = requests.post(URL, json=obj)
        print(x.text)
        iterator += 1
        # break


def main():
    # insert_into_teams()
    # insert_into_leagues()
    # insert_into_player()
    # insert_into_rosters()
    # insert_into_players_defensive()
    # insert_into_players_passing()
    # insert_into_players_offensive()
    # insert_into_players_summary()
    insert_into_league_table()
    insert_into_simple_pythagorean()
    insert_into_extended_pythagorean()


if __name__ == "__main__":
    main()
