import json
import pandas as pd
import numpy as np
from constants import leagues_list
from os import walk, rename
import re
import os


def walk_through_league_tables():  # path_to_league_table):
    df = None
    non_None_df = False
    dict_of_files = walk_through_files("league_table")
    for league in dict_of_files:
        # print(league, '->', dict_of_files[league])
        for season_item in dict_of_files[league]:
            
            split_parts = str(season_item).split('/')
            print(split_parts)
            year_start = split_parts[-1].split('_')[-2]
            year_end = split_parts[-1].split('_')[-1].replace('.csv','')
# Check 2013 2014 they all have missing values so it is not a problem, we just skip them
            if year_start == '2013': 
                continue

            print(f'{league} | {year_start} | {year_end}')

            if(non_None_df == False):
                df = pd.read_csv(season_item)
                df['league'] = league
                df['year_start'] = year_start
                df['year_end'] = year_end
                print(df)
                non_None_df = True
            else:
                df_append = pd.read_csv(season_item)
                df_append['league'] = league
                df_append['year_start'] = year_start
                df_append['year_end'] = year_end
                print("APPEND")
                print(df_append)
                df = df.append(df_append, ignore_index=True)

    print(df)
    df.to_csv('./converted_files/league_table_teamplate.csv')
    zeros = len(df[df.PTS == 0])
    print('PTS O :')
    print(zeros)

    # for file_name in list_of_files:
    #     print(file_name)
    #     # split_parts = str(file_name).split('/')
    #     # league_name = split_parts[3]
    #     # season = split_parts[4].split('_')[-2:-1]
    #     # print(league_name)
    #     # print(season)
    # # return


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



# print(walk_through_files("league_table"))
walk_through_league_tables()

