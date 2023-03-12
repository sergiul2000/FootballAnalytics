import json
import pandas as pd
import numpy as np
from constants import leagues_list
from os import walk, rename


def generate_fixtures_and_clean_sheets_dataframes(path_to_json, path_to_fixtures, path_to_clean_sheets):
    # json_file_path = "jsons/fixtures/epl/epl_fixtures_in_season_2018_2019.json"
    # path_to_fixtures = "dataframes/understat/fixtures/epl/epl_fixtures_in_season_2018_2019.json"
    # path_to_clean_sheets = "dataframes/understat/clean_sheets/epl/epl_fixtures_in_season_2018_2019.json"

    fixtures_df = pd.DataFrame(columns=['match_id', 'home_team_id', 'home_team', 'home_short_title',
                               'away_team_id', 'away_team', 'away_short_title', 'home_goals', 'away_goals', 'datetime'])
    dict_teams = dict()

    with open(path_to_json, 'r') as j:
        contents = json.loads(j.read())
        index = 0
        for item in contents:
            fixtures_df.at[index, 'match_id'] = item['id']
            fixtures_df.at[index, 'home_team'] = item['h']['title']
            fixtures_df.at[index, 'away_team'] = item['a']['title']
            fixtures_df.at[index, 'home_team_id'] = item['h']['id']
            fixtures_df.at[index, 'away_team_id'] = item['a']['id']
            fixtures_df.at[index,
                           'home_short_title'] = item['h']['short_title']
            fixtures_df.at[index,
                           'away_short_title'] = item['a']['short_title']
            fixtures_df.at[index, 'home_goals'] = item['goals']['h']
            fixtures_df.at[index, 'away_goals'] = item['goals']['a']
            fixtures_df.at[index, 'datetime'] = item['datetime']
            index += 1
            dict_teams[item['h']['id']] = item['h']['title']

    clean_sheets_df = pd.DataFrame(dict_teams.items(), columns=[
                                   'team_id', 'team_name'])
    clean_sheets_df['clean_sheets'] = 0

    # print(clean_sheets_df)

    for index, row in fixtures_df.iterrows():
        home_goals = int(row.home_goals)
        away_goals = int(row.away_goals)
        # print(f'Score {home_goals}  - {away_goals}')

        if (home_goals == 0):
            # print('away clean sheet')
            clean_sheets_df.loc[clean_sheets_df.team_name ==
                                row['away_team'], 'clean_sheets'] += 1
        elif (away_goals == 0):
            # print('home clean sheet')
            clean_sheets_df.loc[clean_sheets_df.team_name ==
                                row['home_team'], 'clean_sheets'] += 1

    # print(clean_sheets_df)

    fixtures_df.to_csv(path_to_fixtures)
    clean_sheets_df.to_csv(path_to_clean_sheets)


def correction_of_all_dataframes(statistic='clean_sheets'):
    """
        Due to bad naming instead of .csv the files had .json
        This function rename thus changing the type of the files automatically
    """
    for league in leagues_list:
        # paths = []
        print(f'LEAGUE {league}')
        for year in range(2014, 2021):
            print(f'Year {year}')
            path = f'dataframes/understat/{statistic}/{league}'

            filenames = next(walk(path), (None, None, []))[2]
            filenames = [f'{path}/{filename}' for filename in filenames]

            filenames = next(walk(path), (None, None, []))[2]
            filenames = [f'{path}/{filename}' for filename in filenames]

            print(filenames)
            for file_name in filenames:
                print(f'File {file_name}')
                new_file_name = file_name.replace('json', 'csv')

                # Correction
                rename(file_name, new_file_name)
                # End of Correction

                # csv = replace_pd(csv)


if __name__ == '__main__':
    correction_of_all_dataframes("fixtures")
