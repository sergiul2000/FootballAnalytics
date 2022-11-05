import pandas as pd
from constants import *

def data_unification(league,team,year_start, year_end,):
    #offensive, defensive, summary,understat: clean_sheet, player_team_stats
    path_offensive=f'{whoscored_offensive_relative_path}/{league}/season_{year_start}_{year_end}/{team.replace(" ","_")}_offensive_stats_in_season_{year_start}_{year_end}.csv'
    path_defensive=f'{whoscored_defensive_relative_path}/{league}/season_{year_start}_{year_end}/{team.replace(" ","_")}_defensive_stats_in_season_{year_start}_{year_end}.csv'
    path_summary=f'{whoscored_summary_relative_path}/{league}/season_{year_start}_{year_end}/{team.replace(" ","_")}_summary_stats_in_season_{year_start}_{year_end}.csv'

    path_clean_sheets=f'{understat_clean_sheets_relative_path}/{league}/{league}_clean_sheets_in_season_{year_start}_{year_end}.csv'
    path_league_table=f'{understat_league_table_relative_path}/{league}/{league}_league_table_in_season_{year_start}_{year_end}.csv'
    path_player_team_stats=f'{understat_player_team_stats_relative_path}/{league}/season_{year_start}_{year_end}/{team}_{league}_players_stats_in_season_{year_start}_{year_end}.csv'


    df_offensive=pd.read_csv(path_offensive)
    df_defensive=pd.read_csv(path_defensive)
    df_summary=pd.read_csv(path_summary)

    df_clean_sheets=pd.read_csv(path_clean_sheets)
    df_league_table=pd.read_csv(path_league_table)
    df_player_stats=pd.read_csv(path_player_team_stats)




data_unification('bundesliga','Bayer Leverkusen', 2015,2016)