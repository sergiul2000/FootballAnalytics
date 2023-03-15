import json
import pandas as pd
import numpy as np
from constants import leagues_list
from os import walk, rename
import re
import os


def walk_through_league_tables():  # path_to_league_table):

    # league_table_df = pd.DataFrame(columns=["league_name", "team_name", "year_start", "year_end", "matches", "wins", "draws",
    #                                         "loses", "goals", "goals_against", "points", "xgoals", "npx_goals"])
    # dict_teams = dict()
    try:
        os.mkdir('./converted_files')
    except OSError as error:
        print(error)
    list_of_files = walk_through_files("league_table")
    year_of_file = re.compile(r'20[0-5][0-9]')
    frames = []
    df_total = pd.DataFrame()
    for league in leagues_list:
        for filename_with_path in list_of_files[league]:
            # print(filename)

            # DE AICI AR TREBUI SA FIE O FUNCTIE CE SA MODIFICE UN FILE INDIVIDUAL CU UN PARAMETRU DE FILE_PATH, YEAR
            mo = year_of_file.search(filename_with_path)
            year_start = mo.group()
            year_end = int(year_start)+1
            # print(year_start)
            df_iterator = pd.read_csv(filename_with_path, usecols=range(0, 18))
            df_iterator.insert(0, 'League', league)
            df_iterator.insert(2, 'Year_start', year_start)
            df_iterator.insert(3, 'Year_end', str(year_end))
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
    df_total.to_csv('./converted_files/league_table.csv')
    print(df_total)
    # return


def walk_through_files(type_of_file):
    list_of_files = {}
    for league in leagues_list:
        path = f'dataframes/understat/{type_of_file}/{league}'

        # aici iau numele fisierului si il pun urmatorul in lista de fisiere
        filenames = next(walk(path), (None, None, []))[2]

        # aici ii pun si path-ul in lista, deoarece eu in final vreau path-ruile spre
        # fisiere, nu doar numele fisierelor
        filename_with_path = [f'{path}/{filename}' for filename in filenames]
        list_of_files[league] = filename_with_path
    return list_of_files


def main():
    # print(walk_through_files("league_table"))
    walk_through_league_tables()


if __name__ == "__main__":
    main()
