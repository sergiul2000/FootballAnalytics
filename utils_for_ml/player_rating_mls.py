from constants import *
import logging
import time
import pandas as pd
pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None

logger = logging.getLogger('my_module_name')


playing_role_map = whoscored_player_position_dict['playing_role']
field_position_map = whoscored_player_position_dict['field_position']
simplified_position_map = whoscored_player_position_dict['simplified_role']


def data_unification(league, team, year_start, year_end,):
    logging.basicConfig(filename=f'debugger_logs/mls_formula_logs.log',
                        encoding='utf-8', level=logging.INFO, filemode='a')
    logging.info(f'Team {team} | Year {year_start}:{year_start + 1}')

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
    df_result = df_offensive[['player_number', 'name', 'position', 'start_games', 'sub_games',
                              'mins', 'goals', 'assists', 'shot_per_game', 'offsides_per_game', 'rating']]
    df_result['total_shots'] = df_result['shot_per_game'] * \
        (df_result['start_games'] + df_result['sub_games'])

    # df_result = df_result.drop( ['Unnamed: 0', 'player_number', 'age', 'tall', 'weight','key_passes_per_game', 'dribbles_per_game', 'fouled_per_game', 'dispossessed_per_game', 'bad_control_per_game' ], axis = 1)

    df_result['team'] = team
    df_result['year_start'] = year_start
    df_result['year_end'] = year_end
    df_result['league'] = league

    # from deffensive
    # name, fouls_per_game
    df_defensive = df_defensive[['name', 'fouls_per_game']]
    # df_defensive.drop(['Unnamed: 0', 'player_number', 'age', 'position', 'tall', 'weight', 'games', ''],axis = 1)
    df_result = pd.merge(df_result, df_defensive, on=['name'])
    df_result['total_fouls'] = df_result['fouls_per_game'] * \
        (df_result['start_games'] + df_result['sub_games'])

    # from summary
    # yellow_cards, red_cards
    df_summary = df_summary[["name", "yellow_cards", "red_cards"]]
    df_result = pd.merge(df_result, df_summary, on=['name'])

    # clean_sheets
    # clean_sheets value for given team
    value_clean_sheets = df_clean_sheets['clean_sheets'].loc[df_clean_sheets['team_name'] == team]
    # print(value_clean_sheets)
    # print(f'CLEAN_SHEETS BY {team} IS {int(value_clean_sheets)}')
    df_result['clean_sheets'] = int(value_clean_sheets)

    # league_table
    # points value for given team
    value_points = df_league_table['PTS'].loc[df_league_table['Team'] == team]
    # print(f'POINTS BY {team} IS {int(value_points)}')
    df_result['points'] = int(value_points)

    # player_team_stats
    # player_name, xG, xGA
    df_player_stats = df_player_stats[["player_name", "xG", "xA"]]
    df_result = pd.merge(df_result, df_player_stats,
                         left_on='name', right_on='player_name')
    df_result = df_result.drop(['player_name'], axis=1)
    df_result = df_result[df_result.columns.drop(
        list(df_result.filter(regex="Unnamed")))]

    # Position processing

    # df_result['main_position'] = df.apply(lambda row: row.Cost - (row.Cost * 0.1), axis = 1)

    df_result['mapped_position'], df_result['number_of_positions'] = zip(
        *df_result['position'].map(map_position))

    # position, games_started, games_sub, minutes_played, points, goals,
    # xGoals, assists, xAssists, shots,
    # offsides_per_game, clean_sheets,
    # total_fouls, yellow_cards, red_cards, number_of_positions_played
    df_result['rating_mls_formula'] = df_result.apply(lambda x: apply_mls_rating_formula(
        name=x['name'],
        position=x['mapped_position'], games_started=x['start_games'], games_sub=x['sub_games'],
        minutes_played=x['mins'], points=x['points'], goals=x['goals'],
        xGoals=x['xG'], assists=x['assists'], xAssists=x['xA'], shots=x['total_shots'],
        offsides_per_game=x['offsides_per_game'], clean_sheets=x['clean_sheets'],
        total_fouls=x['total_fouls'], yellow_cards=x['yellow_cards'], red_cards=x['red_cards'],
        number_of_positions_played=x['number_of_positions']
    ), axis=1)

    df_result = df_result.sort_values(by='rating_mls_formula', ascending=False)

    cols_at_end = ['rating', 'rating_mls_formula']
    df_result = df_result[[c for c in df_result if c not in cols_at_end]
                          + [c for c in cols_at_end if c in df_result]]

    # df_result = df_result.drop(['Unnamed: 0','name','age','position','tall','weight','games','mins','rating'],axis=1)
    # print(df_result.head(30))
    # print(df_result.columns)

    return df_result


def map_position(positions_string):

    positions_string = positions_string.replace(' ', '')
    # print(f'POSITION TO MAP {positions_string}')

    positions = positions_string.split(',')

    number_of_positions_played = len(positions)
    mapped_positions = []

    for position in positions:
        # print(position)
        if '(' in position:

            playing_role = position.split('(')[0]
            playing_role = simplified_position_map[playing_role]

            # Just in case
            field_positions = position.split('(')[1]
            field_positions = field_positions.replace(')', '')
            # Check if left right central are different positions
            number_of_positions_played += len(field_positions)-1

            field_positions = ' '+field_position_map[field_positions]

            # if needed
            # mapped_positions.append(playing_role + field_positions)
            mapped_positions.append(playing_role)
        else:
            playing_role = playing_role_map[position]
            mapped_positions.append(playing_role)

    mapped_positions_string = ' '.join(
        [str(elem) for elem in mapped_positions])

    # print(mapped_positions_string)
    # print(number_of_positions_played)

    return mapped_positions_string, number_of_positions_played


def apply_mls_rating_formula(name, position, games_started, games_sub, minutes_played, points, goals, xGoals,
                             assists, xAssists, shots, offsides_per_game, clean_sheets,
                             total_fouls, yellow_cards, red_cards, number_of_positions_played
                             ):
    # Positive term  computation

    # print(f'Name {name} | {position}')
    logging.info(f'Name {name} | {position}')

    games_started_ratio = games_started / 30
    minutes_played_ratio = minutes_played / ((games_started + games_sub) * 30)
    points_per_minute_played = points / minutes_played

    goals_scaled = 0
    assists_scaled = 0
    team_total_clean_sheets_scaled = 0
    fouls_commited_per_minute_scaled = 0

    # print(f'POSITION PREDEFINED {position}')

    if ' ' in position:
        position = position.split(' ')[0]

    # print(f'POSITION REDEFINED {position}')

    if (position == 'GK'):
        # print('GK 1')
        return 1

    match position:
        case 'Forward':
            goals_scaled = goals / 3
            assists_scaled = assists / 2
            team_total_clean_sheets_scaled = clean_sheets / 30
            fouls_commited_per_minute_scaled = total_fouls / minutes_played
        case 'Midfielder':
            goals_scaled = goals / 2
            assists_scaled = assists / 3
            team_total_clean_sheets_scaled = clean_sheets / 20
            fouls_commited_per_minute_scaled = (
                total_fouls / minutes_played) * 1.5
        case 'Defender':
            goals_scaled = goals
            assists_scaled = assists
            team_total_clean_sheets_scaled = clean_sheets / 10
            fouls_commited_per_minute_scaled = (
                total_fouls / minutes_played) * 2
        case _:
            # GOALKEEPER
            # print('GK')
            goals_scaled = goals
            assists_scaled = assists
            team_total_clean_sheets_scaled = clean_sheets / 10
            fouls_commited_per_minute_scaled = (
                total_fouls / minutes_played) * 2

    if xGoals == 0:
        goals_term = 0
    else:
        goals_term = goals_scaled / xGoals

    if xAssists == 0:
        assist_term = 0
    else:
        assist_term = assists_scaled / xAssists

    if minutes_played == 0:
        goals_per_minute_played = 0
    else:
        goals_per_minute_played = goals / minutes_played

    # find shots on goal
    if shots == 0:
        goals_on_goal = 0
    else:
        goals_on_goal = goals / (shots*0.3)

    assists_per_minute = assists / minutes_played
    if ((games_started + games_sub) == 0) or (offsides_per_game == 0):
        goals_per_offsides = 0
    else:
        goals_per_offsides = goals / \
            (offsides_per_game * (games_started + games_sub))
    # XTShot pos - X Total team clean sheets | until then 30%
    team_total_clean_sheets_scaled /= clean_sheets * \
        ((minutes_played / 90) / (games_started + games_sub))

    # Positive term merge
    # print('POSITIVE TERM')
    logging.info('POSITIVE TERM')
    # print(f'Games_started_ratio {round(games_started_ratio,2)} Minutes_played_ratio {round(minutes_played_ratio,2)} Points_per_minute_played {round(points_per_minute_played,2)} Goal_term {round(goals_term,2)}')
    logging.info(
        f'Games_started_ratio {round(games_started_ratio,2)} Minutes_played_ratio {round(minutes_played_ratio,2)} Points_per_minute_played {round(points_per_minute_played,2)} Goal_term {round(goals_term,2)}')
    # print(f'Assist_term {round(assist_term,2)} Goals_per_minute_played {round(goals_per_minute_played,2)} Goal_on_goal {round(goals_on_goal,2)}')
    logging.info(
        f'Assist_term {round(assist_term,2)} Goals_per_minute_played {round(goals_per_minute_played,2)} Goal_on_goal {round(goals_on_goal,2)}')
    # print(f'Assists_per_minute {round(assists_per_minute,2)} Goals_per_offsides {round(goals_per_offsides,2)} Teams_total_clean_sheets_scaled {round(team_total_clean_sheets_scaled,2)}')
    logging.info(
        f'Assists_per_minute {round(assists_per_minute,2)} Goals_per_offsides {round(goals_per_offsides,2)} Teams_total_clean_sheets_scaled {round(team_total_clean_sheets_scaled,2)}')

    positive_term = games_started_ratio + minutes_played_ratio + points_per_minute_played + goals_term + \
        assist_term + goals_per_minute_played + goals_on_goal + \
        assists_per_minute + goals_per_offsides + team_total_clean_sheets_scaled

    # Negative term computation
    expected_fouls_commited_per_minute = total_fouls * \
        ((minutes_played / 90) / (games_started + games_sub))
    yellow_cards_scaled = yellow_cards / 10
    card_per_minute = (yellow_cards+red_cards)/minutes_played

    # Negative term merge
    # print('NEGATIVE TERM')
    logging.info('NEGATIVE TERM')
    # print(f'Fouls_commited_per_minute_scaled {round(fouls_commited_per_minute_scaled,2)} Expected_fouls_commited_per_minute {round(expected_fouls_commited_per_minute,2)} MUL {round(fouls_commited_per_minute_scaled * expected_fouls_commited_per_minute,2)}')
    logging.info(
        f'Fouls_commited_per_minute_scaled {round(fouls_commited_per_minute_scaled,2)} Expected_fouls_commited_per_minute {round(expected_fouls_commited_per_minute,2)} MUL {round(fouls_commited_per_minute_scaled * expected_fouls_commited_per_minute,2)}')
    # print(f'Yellow_cards_scaled {round(yellow_cards_scaled,2)} Red_cards {round(red_cards,2)} Card_per_minute {round(card_per_minute,2)}')
    logging.info(
        f'Yellow_cards_scaled {round(yellow_cards_scaled,2)} Red_cards {round(red_cards,2)} Card_per_minute {round(card_per_minute,2)}')

    negative_term = (fouls_commited_per_minute_scaled * expected_fouls_commited_per_minute) +\
        yellow_cards_scaled + red_cards + card_per_minute

    bonus = 0.5 if number_of_positions_played > 1 else 0

    # print(f'Pos {round(positive_term,2)} Neg {round(negative_term,2)} Bonus {round(bonus,2)}')
    logging.info(
        f'Pos {round(positive_term,2)} Neg {round(negative_term,2)} Bonus {round(bonus,2)}')
    # print()
    logging.info("________________________________________________________________________________________________________________________________")

    return positive_term - negative_term + bonus


# df = data_unification('epl','Chelsea', 2017,2018)
# df.to_csv("chelsea_2017_2018_rating.csv")
