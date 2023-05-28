import json
import pandas as pd
import numpy as np
from constants import leagues_list

# from constants import who_scored_types_of_stats
from os import walk, rename
import re
import os


def walk_through_league_tables():  # path_to_league_table):
    # league_table_df = pd.DataFrame(columns=["league_name", "team_name", "year_start", "year_end", "matches", "wins", "draws",
    #                                         "loses", "goals", "goals_against", "points", "xgoals", "npx_goals"])
    # dict_teams = dict()
    try:
        os.mkdir("./converted_files")
    except OSError as error:
        print(error)
    list_of_files = walk_through_understat_files("league_table")
    year_of_file = re.compile(r"20[0-5][0-9]")
    frames = []
    df_total = pd.DataFrame()
    for league in leagues_list:
        for filename_with_path in list_of_files[league]:
            # print(filename)

            # DE AICI AR TREBUI SA FIE O FUNCTIE CE SA MODIFICE UN FILE INDIVIDUAL CU UN PARAMETRU DE FILE_PATH, YEAR
            mo = year_of_file.search(filename_with_path)
            year_start = mo.group()
            year_end = int(year_start) + 1
            # print(year_start)
            df_iterator = pd.read_csv(filename_with_path, usecols=range(1, 18))
            df_iterator = df_iterator.sort_index(axis=1)
            df_iterator.insert(17, "League", league)
            df_iterator.insert(0, "Year_end", str(year_end))
            df_iterator.insert(1, "Year_start", year_start)
            # print()
            if year_start != "2013":
                frames.append(df_iterator)

            # print(df)
            # print()

            # for year in range(2013, 2021):
            #     filename = f'{league}_league_table_{year}_{year+1}.csv'
            #     if filename in list_of_files[league]:
            #         print(filename)
            # print(list_of_files[league])
    df_total = pd.concat(frames)
    team_names = df_total["Team"]
    df_total = df_total.drop(columns=["Team"])
    df_total.insert(18, "Team", team_names)
    df_total.to_csv("./converted_files/league_table.csv")
    # print(df_total)
    # return


def walk_through_fixtures():  # path_to_league_table):
    # league_table_df = pd.DataFrame(columns=["league_name", "team_name", "year_start", "year_end", "matches", "wins", "draws",
    #                                         "loses", "goals", "goals_against", "points", "xgoals", "npx_goals"])
    # dict_teams = dict()
    try:
        os.mkdir("./converted_files")
    except OSError as error:
        print(error)
    list_of_files = walk_through_understat_files("fixtures")
    year_of_file = re.compile(r"20[0-5][0-9]")
    frames = []
    df_total = pd.DataFrame()
    for league in leagues_list:
        for filename_with_path in list_of_files[league]:
            # print(filename)

            # DE AICI AR TREBUI SA FIE O FUNCTIE CE SA MODIFICE UN FILE INDIVIDUAL CU UN PARAMETRU DE FILE_PATH, YEAR
            mo = year_of_file.search(filename_with_path)
            year_start = mo.group()
            year_end = int(year_start) + 1
            # print(year_start)
            # , usecols=range(1, 18))
            df_iterator = pd.read_csv(filename_with_path)
            # df_iterator.insert(0, 'League', league)
            # df_iterator.insert(2, 'Year_start', year_start)
            # df_iterator.insert(3, 'Year_end', str(year_end))
            df_iterator = df_iterator.drop(
                columns=[
                    "home_team_id",
                    "home_short_title",
                    "away_team_id",
                    "away_short_title",
                ]
            )
            # print()
            frames.append(df_iterator)

            # print(df)
            # print()

            # for year in range(2013, 2021):
            #     filename = f'{league}_league_table_{year}_{year+1}.csv'
            #     if filename in list_of_files[league]:
            #         print(filename)
            # print(list_of_files[league])
    df_total = pd.concat(frames)
    df_total = df_total.rename(
        columns={
            "match_id": "1_Match_id",
            "away_goals": "2_Away_goals",
            "datetime": "3_Datetime",
            "home_goals": "4_home_goals",
            "away_team": "5_Away_team",
            "home_team": "6_Home_team",
        }
    )
    df_total = df_total.sort_index(axis=1)
    df_total = df_total.rename(
        columns={
            "1_Match_id": "match_id",
            "2_Away_goals": "away_goals",
            "3_Datetime": "datetime",
            "4_home_goals": "home_goals",
            "5_Away_team": "away_team",
            "6_Home_team": "home_team",
        }
    )
    print(df_total)
    df_total.to_csv("./converted_files/fixtures.csv")
    # print(df_total)
    # return


def walk_through_league_tables_for_teams():
    path = "./converted_files/league_table.csv"
    df = pd.read_csv(path)
    df = df["Team"]
    df.drop_duplicates(keep="first", inplace=True)
    df.to_csv("./converted_files/teams.csv")


def walk_through_rosters_players_and_player_summary():
    try:
        os.mkdir("./converted_files")
    except OSError as error:
        print(error)
    list_of_files = walk_through_who_scored_files("player_summary_stats")
    year_of_file = re.compile(r"20[0-5][0-9]")
    frames_players = []
    frames_rosters = []
    frames_player_summary = []
    df_total_players = pd.DataFrame()
    df_total_rosters = pd.DataFrame()
    df_total_player_summary = pd.DataFrame()
    for league in leagues_list:
        for year in range(2009, 2022):
            for filename_with_path in list_of_files[league, year]:
                # print(filename_with_path)
                mo = year_of_file.search(filename_with_path)
                year_start = mo.group()
                year_end = int(year_start) + 1
                # print(year_start)
                df_iterator_players = pd.read_csv(
                    filename_with_path
                )  # , usecols=range(1, 18))
                team = filename_with_path.split(f"{year+1}/")[1]
                team = team.split("_s")[0]
                team = team.replace("_", " ")
                # print(team)
                df_iterator_players.insert(1, "Team", team)
                df_iterator_players.insert(3, "Year_start", year_start)
                df_iterator_players.insert(4, "Year_end", str(year_end))

                df_rosters = pd.DataFrame()
                # df_rosters.insert(5, "Year_end", str(year_end))
                df_rosters["Year_end"] = df_iterator_players["Year_end"]
                df_rosters["Year_start"] = df_iterator_players["Year_start"]
                df_rosters["Player_id"] = df_iterator_players["player_number"]
                df_rosters["Team"] = df_iterator_players["Team"]
                df_rosters["League"] = league

                df_player_summary = pd.DataFrame()
                df_player_summary["Team"] = df_iterator_players["Team"]
                df_player_summary["player_number"] = df_iterator_players[
                    "player_number"
                ]
                df_player_summary["Year_start"] = df_iterator_players["Year_start"]
                df_player_summary["Year_end"] = df_iterator_players["Year_end"]
                df_player_summary["games"] = df_iterator_players["games"]
                df_player_summary["start_games"] = df_iterator_players["start_games"]
                df_player_summary["sub_games"] = df_iterator_players["sub_games"]
                df_player_summary["mins"] = df_iterator_players["mins"]
                df_player_summary["goals"] = df_iterator_players["goals"]
                df_player_summary["assists"] = df_iterator_players["assists"]
                df_player_summary["yellow_cards"] = df_iterator_players["yellow_cards"]
                df_player_summary["red_cards"] = df_iterator_players["red_cards"]
                df_player_summary["shots_per_game"] = df_iterator_players[
                    "shots_per_game"
                ]
                df_player_summary["pass_success_percentage"] = df_iterator_players[
                    "pass_success_percentage"
                ]
                df_player_summary["aerials_won"] = df_iterator_players["aerials_won"]
                df_player_summary["man_of_the_match"] = df_iterator_players[
                    "man_of_the_match"
                ]
                df_player_summary["rating"] = df_iterator_players["rating"]
                df_iterator_players = df_iterator_players.drop(
                    columns=[
                        "Team",
                        "Year_start",
                        "Year_end",
                        "games",
                        "start_games",
                        "sub_games",
                        "mins",
                        "goals",
                        "assists",
                        "yellow_cards",
                        "red_cards",
                        "shots_per_game",
                        "pass_success_percentage",
                        "aerials_won",
                        "man_of_the_match",
                        "rating",
                    ]
                )
                # df_iterator_players['position'] = df_iterator_players['position']

                frames_player_summary.append(df_player_summary)
                frames_players.append(df_iterator_players)
                frames_rosters.append(df_rosters)
    # print(df_player_summary)
    df_total_players = pd.concat(frames_players)
    df_total_players = df_total_players.drop_duplicates("player_number")
    df_total_players = df_total_players.rename(
        columns={"player_number": "id", "tall": "height"}
    )
    df_total_players = df_total_players.sort_index(axis=1)

    df_total_players.to_csv("./converted_files/players.csv")
    # print(df_total_players)

    df_total_rosters = pd.concat(frames_rosters)
    list_roster_id = list(range(1, len(df_total_rosters.index) + 1, 1))
    df_total_rosters.insert(0, "id_roster", list_roster_id)
    # df_total_rosters["id_roster"] = list_roster_id
    df_total_rosters.to_csv("./converted_files/rosters.csv")
    # print(df_rosters)

    df_total_player_summary = pd.concat(frames_player_summary)
    df_total_player_summary.to_csv("./converted_files/player_summary_stats.csv")


def walk_through_player_defensive_stats():
    try:
        os.mkdir("./converted_files")
    except OSError as error:
        print(error)
    list_of_files = walk_through_who_scored_files("player_defensive_stats")
    year_of_file = re.compile(r"20[0-5][0-9]")
    frames_player_defensive = []
    df_total = pd.DataFrame()
    for league in leagues_list:
        for year in range(2009, 2022):
            for filename_with_path in list_of_files[league, year]:
                # print(filename_with_path)
                mo = year_of_file.search(filename_with_path)
                year_start = mo.group()
                year_end = int(year_start) + 1
                # print(year_start)
                df_iterator_players = pd.read_csv(
                    filename_with_path, usecols=range(2, 21)
                )
                df_iterator_players = df_iterator_players.sort_index(axis=1)
                team = filename_with_path.split(f"{year+1}/")[1]
                team = team.split("_d")[0]
                team = team.replace("_", " ")
                # print(team)

                df_iterator_players = df_iterator_players.drop(
                    columns=[
                        "games",
                        "start_games",
                        "sub_games",
                        "name",
                        "age",
                        "tall",
                        "position",
                        "weight",
                        "mins",
                        "rating",
                    ]
                )

                df_iterator_players.insert(9, "Team", team)
                df_iterator_players.insert(10, "Year_end", str(year_end))
                df_iterator_players.insert(11, "Year_start", year_start)

                frames_player_defensive.append(df_iterator_players)
    # print(df_player_summary)
    df_total = pd.concat(frames_player_defensive)
    # df_total = df_total.sort_index(axis=1)
    print(df_total)
    df_total.to_csv("./converted_files/players_defensive_stats.csv")
    # print(df_total_players)


def walk_through_player_offensive_stats():
    try:
        os.mkdir("./converted_files")
    except OSError as error:
        print(error)
    list_of_files = walk_through_who_scored_files("player_offensive_stats")
    year_of_file = re.compile(r"20[0-5][0-9]")
    frames_player_offensive = []
    df_total = pd.DataFrame()
    for league in leagues_list:
        for year in range(2009, 2022):
            for filename_with_path in list_of_files[league, year]:
                # print(filename_with_path)
                mo = year_of_file.search(filename_with_path)
                year_start = mo.group()
                year_end = int(year_start) + 1
                # print(year_start)
                df_iterator_players = pd.read_csv(
                    filename_with_path, usecols=range(2, 21)
                )
                team = filename_with_path.split(f"{year+1}/")[1]
                team = team.split("_o")[0]
                team = team.replace("_", " ")
                # print(team)
                df_iterator_players = df_iterator_players.rename(
                    columns={"player_number": "id_player"}
                )

                df_iterator_players = df_iterator_players.drop(
                    columns=[
                        "games",
                        "start_games",
                        "sub_games",
                        "name",
                        "age",
                        "goals",
                        "assists",
                        "key_passes_per_game",
                        "shot_per_game",
                        "tall",
                        "position",
                        "weight",
                        "mins",
                    ]
                )  # , "rating"])
                df_iterator_players = df_iterator_players.sort_index(axis=1)
                df_iterator_players.insert(6, "Team", team)
                df_iterator_players.insert(7, "Year_end", str(year_end))
                df_iterator_players.insert(8, "Year_start", year_start)

                frames_player_offensive.append(df_iterator_players)
    # print(df_player_summary)
    df_total = pd.concat(frames_player_offensive)
    df_total.to_csv("./converted_files/players_offensive_stats.csv")
    # print(df_total_players)


def walk_through_player_passing_stats():
    try:
        os.mkdir("./converted_files")
    except OSError as error:
        print(error)
    list_of_files = walk_through_who_scored_files("player_passing_stats")
    year_of_file = re.compile(r"20[0-5][0-9]")
    frames_player_passing = []
    df_total = pd.DataFrame()
    for league in leagues_list:
        for year in range(2009, 2022):
            for filename_with_path in list_of_files[league, year]:
                # print(filename_with_path)
                mo = year_of_file.search(filename_with_path)
                year_start = mo.group()
                year_end = int(year_start) + 1
                # print(year_start)
                df_iterator_players = pd.read_csv(
                    filename_with_path, usecols=range(2, 19)
                )
                team = filename_with_path.split(f"{year+1}/")[1]
                team = team.split("_p")[0]
                team = team.replace("_", " ")
                # print(team)
                df_iterator_players.insert(0, "Team", team)
                df_iterator_players.insert(2, "Year_start", year_start)
                df_iterator_players.insert(3, "Year_end", str(year_end))

                df_iterator_players = df_iterator_players.drop(
                    columns=[
                        "games",
                        "start_games",
                        "sub_games",
                        "name",
                        "age",
                        "total_assists",
                        "pass_success_percentage",
                        "tall",
                        "position",
                        "weight",
                        "mins",
                    ]
                )  # , "rating"])

                frames_player_passing.append(df_iterator_players)
    # print(df_player_summary)
    df_total = pd.concat(frames_player_passing)
    df_total.to_csv("./converted_files/players_passing_stats.csv")
    # print(df_total_players)


def walk_through_who_scored_files(type_of_file):
    list_of_files = {}
    for league in leagues_list:
        for year in range(2009, 2022):
            path = f"dataframes/whoscored_stats/{type_of_file}/{league}/season_{year}_{year+1}"
            # print(path)
            # for type_of_stats in who_scored_types_of_stats:

            # aici iau numele fisierului si il pun urmatorul in lista de fisiere
            filenames = next(walk(path), (None, None, []))[2]

            # aici ii pun si path-ul in lista, deoarece eu in final vreau path-ruile spre
            # fisiere, nu doar numele fisierelor
            filename_with_path = [f"{path}/{filename}" for filename in filenames]
            # print(filename_with_path)
            list_of_files[league, year] = filename_with_path
    return list_of_files


def walk_through_understat_files(type_of_file):
    list_of_files = {}
    for league in leagues_list:
        path = f"dataframes/understat/{type_of_file}/{league}"

        # aici iau numele fisierului si il pun urmatorul in lista de fisiere
        filenames = next(walk(path), (None, None, []))[2]

        # aici ii pun si path-ul in lista, deoarece eu in final vreau path-ruile spre
        # fisiere, nu doar numele fisierelor
        filename_with_path = [f"{path}/{filename}" for filename in filenames]
        list_of_files[league] = filename_with_path
    return list_of_files


def main():
    # print(walk_through_files("league_table"))
    # walk_through_league_tables()
    # walk_through_league_tables_for_teams()
    walk_through_rosters_players_and_player_summary()
    # walk_through_player_defensive_stats()
    # walk_through_player_offensive_stats()
    # walk_through_player_passing_stats()


if __name__ == "__main__":
    main()
