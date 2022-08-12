import json
import pandas as pd
import numpy as np

def generate_fixtures_and_clean_sheets_dataframes(path_to_json, path_to_fixtures, path_to_clean_sheets):
    #json_file_path = "jsons/fixtures/epl/epl_fixtures_in_season_2018_2019.json"
    #path_to_fixtures = "dataframes/fixtures/epl/epl_fixtures_in_season_2018_2019.json"
    #path_to_clean_sheets = "dataframes/clean_sheets/epl/epl_fixtures_in_season_2018_2019.json"

    fixtures_df = pd.DataFrame(columns = ['match_id', 'home_team_id', 'home_team', 'home_short_title', 'away_team_id', 'away_team','away_short_title', 'home_goals', 'away_goals', 'datetime'])
    dict_teams= dict()

    with open(path_to_json, 'r') as j:
        contents = json.loads(j.read())
        index = 0
        for item in contents:
            fixtures_df.at[index, 'match_id'] = item['id']
            fixtures_df.at[index, 'home_team'] = item['h']['title']
            fixtures_df.at[index, 'away_team'] = item['a']['title']
            fixtures_df.at[index, 'home_team_id'] = item['h']['id']
            fixtures_df.at[index, 'away_team_id'] = item['a']['id']
            fixtures_df.at[index, 'home_short_title']= item['h']['short_title']
            fixtures_df.at[index, 'away_short_title']= item['a']['short_title']
            fixtures_df.at[index, 'home_goals']= item['goals']['h']
            fixtures_df.at[index, 'away_goals']= item['goals']['a']
            fixtures_df.at[index, 'datetime'] = item['datetime']
            index+=1
            dict_teams[item['h']['id']] = item['h']['title']

    clean_sheets_df = pd.DataFrame(dict_teams.items(), columns = ['team_id','team_name']) 
    clean_sheets_df['clean_sheets'] = 0

    # print(clean_sheets_df)

    for index,row in fixtures_df.iterrows():
        home_goals = int(row.home_goals)
        away_goals = int(row.away_goals)
        # print(f'Score {home_goals}  - {away_goals}')

        if(home_goals == 0): 
            # print('away clean sheet')
            clean_sheets_df.loc[clean_sheets_df.team_name == row['away_team'], 'clean_sheets' ]+=1
        elif(away_goals == 0):    
            # print('home clean sheet')
            clean_sheets_df.loc[clean_sheets_df.team_name == row['home_team'], 'clean_sheets' ]+=1

    #print(clean_sheets_df)

    fixtures_df.to_csv(path_to_fixtures)
    clean_sheets_df.to_csv(path_to_clean_sheets)

