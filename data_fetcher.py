import pandas as pd
import pandas_datareader.data as web
import asyncio
import json

import aiohttp

from understat import Understat

from empty_folder_creator import create_empty_directories
from constants import league_teams_dict, leagues_list
import fixtures_json_parser


def test_def():
    create_empty_directories("dataframes", "test_stat", "epl", 2014, 2022, True)


async def get_fixtures_in_league_for_season(league, start_year, end_year):
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        understat = Understat(session)

        # generate empy folders for jsons
        create_empty_directories(
            "jsons", "fixtures", league, start_year, end_year, False, True
        )
        # generate empy folders for dataframes
        create_empty_directories(
            "dataframes", "fixtures", league, start_year, end_year, False, True
        )
        create_empty_directories(
            "dataframes", "clean_sheets", league, start_year, end_year, False, True
        )

        for year in range(start_year, end_year):
            print(f"FIXTURE IN LEAGUE {league} SEASON {year}_{year+1}")

            path_season = f"season_{year}_{year+1}"

            data = await understat.get_league_results(
                league,
                year,
            )
            # print(data)

            with open(
                f"demo\\jsons\\fixtures\\{league}\\{league}_fixtures_in_{path_season}.json",
                "w",
            ) as outfile:
                json.dump(data, outfile)
            print(
                "________________________________________________________________________________________________________________________________"
            )

            # fixtures_json_parser.test()

            fixtures_json_parser.generate_fixtures_and_clean_sheets_dataframes(
                f"demo\\jsons\\fixtures\\{league}\\{league}_fixtures_in_{path_season}.json",
                f"demo\\dataframes\\fixtures\\{league}\\{league}_fixtures_in_{path_season}.csv",
                f"demo\\dataframes\\clean_sheets\\{league}\\{league}_clean_sheets_in_{path_season}.csv",
            )


async def get_players_team_statistics_for_choosen_teams_in_league(
    league, teams_list, start_year, end_year
):
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        understat = Understat(session)

        # generate empy folders for jsons
        create_empty_directories(
            "jsons", "player_team_stats", league, start_year, end_year
        )
        # generate empy folders for dataframes
        create_empty_directories(
            "dataframes", "player_team_stats", league, start_year, end_year
        )

        for year in range(start_year, end_year):
            for team_name in teams_list:
                print(
                    f"PLAYER TEAM STAT FOR {team_name} IN LEAGUE {league} SEASON {year}_{year+1}"
                )

                path_season = f"season_{year}_{year+1}"

                data = await understat.get_league_players(
                    league, year, {"team_title": team_name}
                )
                # print(json.dumps(data))
                team_name_string = team_name.replace(" ", "_")
                print(team_name_string)

                with open(
                    f"jsons/player_team_stats/{league}/{path_season}/{team_name}_{league}_players_stats_in_{path_season}.json",
                    "w",
                ) as outfile:
                    json.dump(data, outfile)

                print(
                    "________________________________________________________________________________________________________________________________"
                )
                df = pd.read_json(
                    f"jsons/player_team_stats/{league}/{path_season}/{team_name}_{league}_players_stats_in_{path_season}.json"
                )
                df.to_csv(
                    f"dataframes/player_team_stats/{league}/{path_season}/{team_name}_{league}_players_stats_in_{path_season}.csv"
                )
                print(df.head(5))


async def get_league_table(league, start_year, end_year):
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        understat = Understat(session)

        # generate empy folders for jsons
        create_empty_directories(
            "jsons", "league_table", league, start_year, end_year, False
        )
        # generate empy folders for dataframes
        create_empty_directories(
            "dataframes", "league_table", league, start_year, end_year, False
        )

        for year in range(start_year, end_year):
            print(f"LEAGUE TABLE FOR {league} SEASON {year}_{year+1}")

            path_season = f"season_{year}_{year+1}"

            data = await understat.get_league_table(league, year)
            print(data)

            with open(
                f"demo\\jsons\\league_table\\{league}\\{league}_league_table_in_{path_season}.json",
                "w",
            ) as outfile:
                json.dump(data, outfile)
            print(
                "________________________________________________________________________________________________________________________________"
            )

            df = pd.read_json(
                f"demo\\jsons\\league_table\\{league}\\{league}_league_table_in_{path_season}.json"
            )

            # first row contains columns problem
            df.columns = df.iloc[0]
            df = df[1:]

            df.to_csv(
                f"demo\\dataframes\\league_table\\{league}\\{league}_league_table_in_{path_season}.csv"
            )

            print(df.head(5))


if __name__ == "__main__":
    # for league, teams_list in league_teams_dict.items():
    #     print(f'{league} : {teams_list}')

    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(get_players_team_statistics_for_choosen_teams_in_league(league, teams_list,2014,2022))

    # for league in leagues_list:
    #     print(league)
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(get_league_table(league,2014,2022))

    for league in leagues_list:
        print(league)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_league_table(league, 2014, 2016))
