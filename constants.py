
# UNDERSTAT CONSTANTS

leagues_list = ['epl', # Premier League
           'bundesliga',
           'la liga',
           'ligue 1',
           'serie a',
           ]

league_teams_dict = {'epl' : ["Manchester United", "Manchester City", "Chelsea", "Liverpool", "Arsenal", "Tottenham"],
           'bundesliga' : ["Bayern Munich", "Borussia Dortmund", "Bayer Leverkusen", "RasenBallsport Leipzig", "Eintracht Frankfurt", "Wolfsburg"],
           'la liga' : ["Real Madrid", "Barcelona", "Atletico Madrid", "Sevilla", "Valencia", "Villarreal"],
           'ligue 1' : ["Paris Saint Germain", "Marseille", "Monaco", "Nice", "Rennes", "Lyon"],
           'serie a' : ["Juventus", "Inter", "AC Milan", "Napoli", "Roma", "Atalanta"]
           }


# WHOSCORED CONSTANTS

API_DELAY_FOR_YOUR_PC = 0.5

who_scored_simple_columns = {
    'summary' : ["goals", "assists", "yellow_cards", "red_cards", "shots_per_game", "pass_success_percentage", "aerials_won_per_game", "man_of_the_match"],
    'defensive' : ["tackles_per_game", "interceptions_per_game", "fouls_per_game", "offsides_won_per_game","clearances_per_game", "dribbled_past_per_game", "outfielder_blocks_per_game", "own_goals"],
    'offensive' : ["goals", "assists", "shot_per_game", "key_passes_per_game", "dribbles_per_game", "fouled_per_game", "offsides_per_game", "dispossessed_per_game", "bad_control_per_game"],
    'passing' : ["total_assists", "key_passes_per_game", "passes_per_game", "pass_success_percentage", "crosses_per_game", "long_ball_per_game", "through_balls_per_game"],
}

whoscored_teams_dict = {
           'la liga' : 
           {
            "Real Madrid"       : 52, 
            "Barcelona"         : 65, 
            "Atletico Madrid"   : 63, 
            "Sevilla"           : 67, 
            "Valencia"          : 55, 
            "Villarreal"        : 839,
            },

           'epl' : 
           {
            "Manchester United" : 32, 
            "Manchester City"   : 167, 
            "Chelsea"           : 15,
            "Liverpool"         : 26, 
            "Arsenal"           : 13,
            "Tottenham"         : 30,
           },

           'bundesliga' : 
           {
            "Bayern Munich"          : 37, 
            "Borussia Dortmund"      : 44,
            "Bayer Leverkusen"       : 36, 
            "RasenBallsport Leipzig" : 7614,
            "Eintracht Frankfurt"    : 45,
            "Wolfsburg"              : 33,
           },

           'ligue 1' : 
           {
            "Paris Saint Germain" : 304, 
            "Marseille"           : 249, 
            "Monaco"              : 248, 
            "Nice"                : 613, 
            "Rennes"              : 313, 
            "Lyon"                : 228,
            },

           'serie a' : 
           {
            "Juventus"  : 87, 
            "Inter"     : 75, 
            "AC Milan"  : 80, 
            "Napoli"    : 276, 
            "Roma"      : 84, 
            "Atalanta"  : 300,
           }
}

whoscored_player_position_dict = {
    'playing_role':
    {
        "AM" : "Attacking Midfielder",
        "FW" : "Forward",
        "D" : "Defender",
        "M" : "Midfielder",
        "GK" : "Goalkeeper",
        "DMC" : "Defensive Midfielder",
        "Midfielder" : "Midfielder",
        "Forward" : "Forward",
        "Defender" : "Defender",
    },

    'simplified_role':
    {
        "AM" : "Midfielder",
        "FW" : "Forward",
        "D" : "Defender",
        "M" : "Midfielder",
        "GK" : "Goalkeeper",
        "DMC" : "Midfielder",
        "Midfielder" : "Midfielder",
        "Forward" : "Forward",
        "Defender" : "Defender",
    },

    'field_position':
    {
        "CLR" : "Central Left Right" ,
        "CL" : "Central Left",
        "CR" : "Central Right",
        "LR" : "Left Right",
        "C" : "Central",
        "L" : "Left",
        "R" : "Right", 
    }
}

# generic stat : stat_subcategory : ([circumstances] , [specific stat])
whoscored_detailed_options = {

    "defensive": {
        "Tackles" : ([], (["tackles_won", "player_gets_dribble_past", "tackles_attempts"])),
        "Interception" : ([], (["total_interceptions"])),
        "Fouls" : ([], (["fouled", "fouls_commited"])),
        "Cards" : ([], (["yellow_cards", "red_card"])),
        "Offsides" : ([], (["caught_offside"])),
        "Clearances" : ([], (["clearances"])),
        "Blocks" : ([], (["shots_blocked", "crosses_blocked", "passes_blocked"])),
        "Saves" : ([], (["total_saves", "six_yard_box_saves", "penalty_area_saves", "saves_from_outside_the_box"])),
    },

    "offensive" : {
        "Shots" : (["Zones", "Situations", "Accuracy", "Body Parts"], 
                    (
                    ["total_shots", "box_shots_from_outside_penalty_area", "inside_six_yard_box_shots", "inside_the_penalty_area_shots"],
                    ["total_shots", "open_play_shots", "counter_attack_shots", "set_pieces_shots", "penalties_taken"],
                    ["total_shots", "off_target_shots", "on_post_shots", "on_target_shots", "blocked_shots"],
                    ["total_shots", "right_foot_shots", "left_foot_shots", "headers_shots", "other_body_part_shots"],
                    )
                ),
        "Goals" : (["Zones", "Situations", "Body Parts"], 
                   (
                   ["total_goals", "inside_six_yard_box_goals", "inside_penalty_area_goals", "outside_penalty_area_goals"],
                   ["total_goals", "open_play_goals", "counter_attack_goals", "set_piece_goals", "penalties_scored", "own_goals", "normal_goals"],
                   ["total_goals", "right_foot_goals", "left_foot_goals", "headers_goals", "other_goals"],
                   )
                ),
        "Dribbles" : ([], (["unsuccesful_dribbles", "succesful_dribbles", "total_dribbles"])),
        "Possession loss" : ([], (["unsuccessful_touches", "dispossessed"])),
        "Aerial" : ([], (["total_aerials", "won_aerials", "lost_aerials"])),
    },

    "passing" : {
        "Passes" : (["Length", "Type"], 
                    ( 
                    ["total_passes", "accurate_long_ball_passes", "inaccurate_long_ball_passses", "accurate_short_passes", "inaccurate_short_passes"], 
                    ["accurate_cross_passes", "inaccurate_cross_passes", "accurate_corner_passes", "inaccurate_corner_passes", "accurate_freekicks", "innaccurate_freekicks"]
                    ) 
                    ),
        "Key passes" : (["Length", "Type"], 
                        (
                        ["total_key_passes", "long_passes", "short_passes"], 
                        ["cross_passes", "corner_passes", "throughball_passes", "freekick_passes", "throwin_passes", "other_passes"]
                        )
                       ),
        "Assists" : ([], (["cross_assist", "corner_assist", "throughball_assist", "freekick_assist", "throwin_assist", "other_assists", "total_assists"])),
    }

}

# realative path
whoscored_summary_relative_path = 'dataframes/whoscored_stats/player_summary_stats'
whoscored_offensive_relative_path  = 'dataframes/whoscored_stats/player_offensive_stats'
whoscored_defensive_relative_path  = 'dataframes/whoscored_stats/player_defensive_stats'
whoscored_passing_relative_path  = 'dataframes/whoscored_stats/player_passing_stats'

understat_clean_sheets_relative_path  = 'dataframes/understat/clean_sheets'
understat_league_table_relative_path  = 'dataframes/understat/league_table'
understat_player_team_stats_relative_path  = 'dataframes/understat/player_team_stats'



# for category, subcategory_mapping in whoscored_detailed_options.items():
#     print(f" BIG STAT {category}")
#     for subcategory, conditions  in subcategory_mapping.items():

#         #print(condition)
#         if(conditions[0]==[]):
#             #print(conditions)
#             print(f'None -> {conditions[1]}')

#         else:
#             #print(conditions)
#             characteristics = conditions[0]
#             index_columns = 0
#             for characteristic in  characteristics:
#                 print(f'{characteristic} -> {conditions[1][index_columns]}')
#                 index_columns +=1

# category = 'passing'
# subcategory_mapping = whoscored_detailed_options[category]
# for subcategory, conditions  in subcategory_mapping.items():

#     print(subcategory)
#     if(conditions[0]==[]):
#         #print(conditions)
#         columns = conditions[1]
#         print(f'None -> {columns}')

#     else:
#         #print(conditions)
#         characteristics = conditions[0]
#         columns = conditions[1]
#         index_columns = 0
#         for characteristic in  characteristics:
#             print(f'{characteristic} -> {columns[index_columns]}')
#             index_columns +=1
