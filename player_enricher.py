import pandas as pd

from empty_folder_creator import create_empty_directories
from constants import league_teams_dict, leagues_list


def fetch_players_for_season(league, team_list, start_year, end_year):

    for year in range(start_year, end_year):
        path_season = f'season_{year}_{year+1}'

        for team_name in teams_list:
            print(f'{team_name} {start_year} {end_year}')
            # team_name_string = team_name.replace(" ", "_")

            player_team_stats_path = f'dataframes/understat/player_team_stats/{league}/{path_season}/{team_name}_{league}_players_stats_in_{path_season}.csv'
            # print(player_team_stats_path)
            df_player_team_stats = pd.read_csv(player_team_stats_path)
            print(df_player_team_stats)

            clean_sheets_path = f'dataframes/understat/clean_sheets/{league}/{league}_clean_sheets_in_{path_season}.csv'
            df_clean_sheets = pd.read_csv(clean_sheets_path)
            print(df_clean_sheets)

            df_player_perfomance = pd.DataFrame(
                columns=['player_id', 'player_name', 'games_started', 'minutes_per_game', ''])

    index = 0
    # interate and add clean sheets plus the other metrics
    '''
    games_started, minutes_per_game, team_points_per_minute, goals, expected_goals, assists, expected_assists,
                                   goals_per_minute, goals_per_shot_on_goal, assists_per_minute, goals_per_offside_offense,
                                   total_wins_by_zero, expected_total_wins_by_zero, fouls_commited_per_minute, expected_fouls_commited_per_minute,
                                   yellow_cards, red_cards, total_cards_per_minute, bonus):

    '''
    fixtures_df.at[index, 'match_id'] = item['id']


if __name__ == "__main__":

    for league, teams_list in league_teams_dict.items():
        print(f'{league} : {teams_list}')

        fetch_players_for_season(league, teams_list, 2014, 2022)

        break
