from math import gamma
import pandas as pd
from constants import *

playing_role_map = whoscored_player_position_dict['playing_role']
field_position_map = whoscored_player_position_dict['field_position']
simplified_position_map = whoscored_player_position_dict['simplified_role']

def data_unification(league,team,year_start, year_end,):
    # Path generation for whoscored and understat dataframes
    # whoscored: offensive, defensive, summary,
    # understat: clean_sheet, player_team_stats
    path_offensive = f'{whoscored_offensive_relative_path}/{league}/season_{year_start}_{year_end}/{team.replace(" ","_")}_offensive_stats_in_season_{year_start}_{year_end}.csv'
    path_defensive = f'{whoscored_defensive_relative_path}/{league}/season_{year_start}_{year_end}/{team.replace(" ","_")}_defensive_stats_in_season_{year_start}_{year_end}.csv'
    path_summary = f'{whoscored_summary_relative_path}/{league}/season_{year_start}_{year_end}/{team.replace(" ","_")}_summary_stats_in_season_{year_start}_{year_end}.csv'

    path_clean_sheets = f'{understat_clean_sheets_relative_path}/{league}/{league}_clean_sheets_in_season_{year_start}_{year_end}.csv'
    path_league_table = f'{understat_league_table_relative_path}/{league}/{league}_league_table_in_season_{year_start}_{year_end}.csv'
    path_player_team_stats = f'{understat_player_team_stats_relative_path}/{league}/season_{year_start}_{year_end}/{team}_{league}_players_stats_in_season_{year_start}_{year_end}.csv'


    # Reading the dataframes needed
    df_offensive = pd.read_csv(path_offensive)
    df_defensive = pd.read_csv(path_defensive)
    df_summary = pd.read_csv(path_summary)

    df_clean_sheets = pd.read_csv(path_clean_sheets)
    df_league_table = pd.read_csv(path_league_table)
    df_player_stats = pd.read_csv(path_player_team_stats)

    # Merger of the dataframes

    # from offensive 
    # games, position, start_games, sub_games, mins, goals, assists, shot_per_game, offsides_per_game
    df_result = df_offensive [['name','position', 'start_games','sub_games', 'mins', 'goals', 'assists', 'shot_per_game', 'offsides_per_game']]

    #df_result = df_result.drop( ['Unnamed: 0', 'player_number', 'age', 'tall', 'weight','key_passes_per_game', 'dribbles_per_game', 'fouled_per_game', 'dispossessed_per_game', 'bad_control_per_game' ], axis = 1)

    # from deffensive
    # name, fouls_per_game
    df_defensive = df_defensive[['name', 'fouls_per_game']]
    #df_defensive.drop(['Unnamed: 0', 'player_number', 'age', 'position', 'tall', 'weight', 'games', ''],axis = 1)
    df_result = pd.merge(df_result, df_defensive, on = ['name'])
    df_result['total_fouls']  = df_result['fouls_per_game'] * (df_result['start_games'] + df_result['sub_games'])

    # from summary
    # yellow_cards, red_cards
    df_summary = df_summary [["name", "yellow_cards", "red_cards"]]
    df_result = pd.merge(df_result, df_summary, on = ['name'])

    # clean_sheets
    # clean_sheets value for given team
    value_clean_sheets = df_clean_sheets['clean_sheets'].loc[df_clean_sheets['team_name'] == team]
    print(f'CLEAN_SHEETS BY {team} IS {int(value_clean_sheets)}')
    df_result['clean_sheets'] = int(value_clean_sheets)
    
    # league_table
    # points value for given team
    value_points = df_league_table['PTS'].loc[df_league_table['Team'] == team]
    print(f'POINTS BY {team} IS {int(value_points)}')
    df_result['points'] = int(value_points) 

    # player_team_stats
    # player_name, xG, xGA
    df_player_stats = df_player_stats[["player_name", "xG", "xA"]]
    df_result = pd.merge(df_result, df_player_stats, left_on='name', right_on='player_name')

    df_result = df_result[df_result.columns.drop(list(df_result.filter(regex = "Unnamed")))]


    # Position processing
    print(df_result['position'])

    #df_result = df_result.drop(['Unnamed: 0','name','age','position','tall','weight','games','mins','rating'],axis=1)
    print(df_result.head(30))
    print(df_result.columns)

    return df_result


def map_position(positions_string):

    positions = positions_string.split(',')

    number_of_positions_played = len(positions) 
    mapped_positions = []

    for position in positions:
        print(position)
        if '(' in position:

            playing_role = position.split('(')[0]
            playing_role = simplified_position_map[playing_role]

            # Just in case
            field_positions = position.split('(')[1]
            field_positions = field_positions.replace(')','')
            number_of_positions_played += len(field_positions)-1
            
            field_positions = ' '+field_position_map[field_positions]

            # if needed
            #mapped_positions.append(playing_role + field_positions)
            mapped_positions.append(playing_role)
        else :
            playing_role = playing_role_map[position]
            mapped_positions.append(playing_role)
 
    mapped_positions_string = ' '.join([str(elem) for elem in mapped_positions])

    return mapped_positions_string, number_of_positions_played

def apply_basic_rating_formula(df):
    return


#df = data_unification('bundesliga','Bayer Leverkusen', 2014,2015)
