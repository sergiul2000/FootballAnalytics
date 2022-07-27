import pandas as pd
import pandas_datareader.data as web
import asyncio
import json

import aiohttp

from understat import Understat 

from empty_folder_creator import create_empty_directories
from constants import league_teams_dict, leagues_list

def test_def():
    create_empty_directories('dataframes','test_stat','epl', 2014, 2022)


async def get_players_team_statistics_for_choosen_teams_in_league(league, teams_list, start_year, end_year):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session: 
        understat = Understat(session)

        #generate empy folders for jsons
        create_empty_directories('jsons', 'player_team_stats', league, start_year, end_year)
        # generate empy folders for dataframes
        create_empty_directories('dataframes', 'player_team_stats', league, start_year, end_year)

        for year in range(start_year, end_year):
            for team_name in teams_list:
                print(f'PLAYER TEAM STAT FOR {team_name} IN LEAGUE {league} SEASON {year}_{year+1}')

                path_season = f'season_{year}_{year+1}'

                data = await understat.get_league_players(league, year, {"team_title": team_name})
                #print(json.dumps(data))
                team_name_string = team_name.replace(" ", "_")
                print(team_name_string)

                with open(f'jsons/player_team_stats/{league}/{path_season}/{team_name}_{league}_players_stats_in_{path_season}.json', 'w') as outfile:
                    json.dump(data, outfile)

                print("________________________________________________________________________________________________________________________________")
                df = pd.read_json(f'jsons/player_team_stats/{league}/{path_season}/{team_name}_{league}_players_stats_in_{path_season}.json')
                df.to_csv(f'dataframes/player_team_stats/{league}/{path_season}/{team_name}_{league}_players_stats_in_{path_season}.csv')
                print(df.head(5))


async def get_league_table(league, start_year, end_year):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        understat = Understat(session)

        #generate empy folders for jsons
        create_empty_directories('jsons', 'league_table', league, start_year, end_year, False)
        # generate empy folders for dataframes
        create_empty_directories('dataframes', 'league_table', league, start_year, end_year, False)

        for year in range(start_year, end_year):
            print(f'LEAGUE TABLE FOR {league} SEASON {year}_{year+1}')

            path_season = f'season_{year}_{year+1}'

            data = await understat.get_league_table(league, year)
            print(data)

            with open(f'jsons/league_table/{league}/{league}_league_table_in_{path_season}.json', 'w') as outfile:
                json.dump(data, outfile)
            print("________________________________________________________________________________________________________________________________")


            df = pd.read_json(f'jsons/league_table/{league}/{league}_league_table_in_{path_season}.json')
            
            # first row contains columns problem solved
            df.columns = df.iloc[0]
            df = df[1:]
            
            df.to_csv(f'dataframes/league_table/{league}/{league}_league_table_in_{path_season}.csv')

            print(df.head(5))




if __name__ == "__main__":
    # for league, teams_list in league_teams_dict.items():
    #     print(f'{league} : {teams_list}')

    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(get_players_team_statistics_for_choosen_teams_in_league(league, teams_list,2014,2022))

    for league in leagues_list:
        print(league)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_league_table(league,2014,2022))





    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(get_players_team_statistics_for_teams_in_league('Paris Saint Germain','ligue 1',2014,2022))





