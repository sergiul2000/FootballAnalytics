import pandas as pd
import pandas_datareader.data as web
import asyncio
import json

import aiohttp

from understat import Understat 



async def get_players_team_statistics_in_given_year(team_name, competition_year, league):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session: 
        understat = Understat(session)
        data = await understat.get_league_players(league, competition_year, {"team_title": team_name})
        #print(json.dumps(data))
        team_name = team_name.replace(" ", "_")
        print(team_name)
        with open(f'jsons/player_team_stats/{league}/{competition_year}/{team_name}_{league}_players_stats_in_{competition_year}.json', 'w') as outfile:
            json.dump(data, outfile)
        print("________________________________________________________________________________________________________________________________")
        df = pd.read_json(f'jsons/player_team_stats/{league}/{competition_year}/{team_name}_{league}_players_stats_in_{competition_year}.json')
        df.to_csv(f'dataframes/player_team_stats/{league}/{competition_year}/{team_name}_{league}_players_stats_in_{competition_year}.csv')

        print(df.head(5))


if __name__ == "__main__":

    list_of_teams = ["Manchester United", "Manchester City", "Chelsea", "Liverpool", "Arsenal", "Tottenham"]

    for year in range(2014,2023):
        for i, team in enumerate(list_of_teams):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(get_player_overall_statistics_by_league_and_year(team, year, 'epl'))


