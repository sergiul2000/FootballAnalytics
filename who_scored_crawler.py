from re import X
from constants import whoscored_teams_dict, whoscored_detailed_options

import time
import pandas as pd
pd.set_option('display.max_columns', None) 
pd.options.mode.chained_assignment = None

import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support.select import Select
from empty_folder_creator import create_empty_directories
from os import walk
import os 



def replace_pd(df):
    mapping = {'-': 0} 
    
    replace_dict = {}
    
    for colum in df.columns:
        replace_dict[colum] = mapping
    return df.replace(replace_dict)



def save_stats_csv(df, stat, league, team, season_start_year):
    print('Saving CSV to File')
    team = team.replace(' ','_')
    filename = f'dataframes/whoscored_player_{stat}_stats/{league}/season_{season_start_year}_{season_start_year+1}/{team}_{stat}_stats_in_season_{season_start_year}_{season_start_year+1}.csv'

    print(filename)
    df.to_csv(filename)


def crawl_chosen_stats_between_years(league, teams_details, start_year, end_year, stat='summary'):

    create_empty_directories('dataframes', f'whoscored_player_{stat}_stats', league, start_year, end_year, True)

    for team, code in teams_details.items():

       # print(team, '->', code)

        dict_of_league_urls = crawl_all_urls_for_given_team_in_league_competitions(code, league, last_season_year= 2022)
        print(f'URLS {team} {code}')
        print(dict_of_league_urls)

        is_current_season = True
        for item in dict_of_league_urls.items():
            print(item)
            
            match stat:
                case 'summary':
                    df_season_summary_stats = crawl_player_team_stats_summary(item[1])
                    
                    save_stats_csv(df_season_summary_stats,'summary',league, team, season_start_year = int(item[0].split('_')[1]))
                case 'offensive':
                    df_season_offensive_stats = crawl_player_team_stats_offensive(item[1], is_current_season)
                    is_current_season = False

                    save_stats_csv(df_season_offensive_stats,'offensive',league, team, season_start_year = int(item[0].split('_')[1]))
                case 'defensive':
                    df_season_defensive_stats = crawl_player_team_stats_defensive(item[1], is_current_season)
                    is_current_season = False

                    save_stats_csv(df_season_defensive_stats,'defensive',league, team, season_start_year = int(item[0].split('_')[1]))
                case 'passing':
                    df_season_passing_stats = crawl_player_team_stats_passing(item[1], is_current_season)
                    is_current_season = False

                    save_stats_csv(df_season_passing_stats,'passing',league, team, season_start_year = int(item[0].split('_')[1]))
                case 'detailed_zones_shots':
                    df_detailed_shots_zones = crawl_player_team_stats_detailed_shots_zones(item[1], is_current_season)
                    is_current_season = False

                    save_stats_csv(df_detailed_shots_zones,'detailed_zones_shots',league, team, season_start_year = int(item[0].split('_')[1]))
                case _:
                    #To Be Implemented
                    print('nada')      

def transform_competition_name(competition_name):
    match competition_name:
        case 'epl':
            competition_text = 'Premier League'
            season_text_start = 'epl_'
        case 'bundesliga':
            competition_text = 'Bundesliga'
            season_text_start = 'bundesliga_'
        case 'la liga':
            competition_text = 'LaLiga'
            season_text_start = 'la liga_'
        case 'ligue 1':
            competition_text = 'Ligue 1'
            season_text_start = 'ligue 1_'
        case 'serie a':
            competition_text = 'Serie A'
            season_text_start = 'seria a_'
        case _:
            competition_text = 'ChampionsLeague'
            season_text_start = 'champions league_'

    return competition_text,season_text_start

def crawl_all_urls_for_given_team_in_league_competitions(team_id, competition_name, last_season_year):
    url_current_season = f'https://www.whoscored.com/Teams/{team_id}'
    url = f'https://www.whoscored.com/Teams/{team_id}/Archive'
    dict_of_league_competitions_urls = dict()
    dict_of_league_competitions_urls[f'{competition_name}_{last_season_year}_{last_season_year+1}'] = url_current_season

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    print('Installing Chrome driver')
    driver.get(url)

    #print(url)
    dropDown = driver.find_element("id","stageId")
    select = Select(dropDown)
    for option in select.options:
        #print(option.get_attribute('value'))
        #print(option.text)
        value = option.get_attribute('value')


        competition_text,season_text_start = transform_competition_name(competition_name)
        
        if competition_text in option.text:
            season_full = option.text.split('-')[1][1:]
            start_year = season_full.split('/')[0]
            end_season = season_full.split('/')[1]
            season_text = f'{start_year}_{end_season}'
            season_text = f'{season_text_start}{season_text}'
            #print(season_text)

            url_to_append = f'https://www.whoscored.com/Teams/{team_id}/Archive/?stageId={value}'
            dict_of_league_competitions_urls[season_text] = url_to_append

   # print("DICT COMPETITIONS URLS:")
    #print(dict_of_league_competitions_urls)
    return dict_of_league_competitions_urls

def establish_driver_connection(url, statistic = 'summary', button_xpath = '//a[contains(@href,"#team-squad-archive-stats-offensive")]', api_delay_term = 1):
    """
    This function establishes connection through a driver object to a specific url of whoscored.
    This also bypasses the accept cookie buttons to unfreeze the next click of the button.
    Also it clicks on the specific button that gets to a specific statistics table.

    Args :
        url : Start url to make connection with a specific part of the website

        statistic : It may be "summary" or "offensive" or "defensive" or "passing"

        button_xpath : This helps to identify the selection button to the specific statistics table

        api_delay_term : Delays the actions in order to wait for the website to load

    return :
        driver : The driver to the page that has already the specific statitics table loaded.

    """
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
    print('Installing Chrome driver')
    driver.get(url)

    # wait for getting data
    print('Waiting for getting data')

    time.sleep(api_delay_term)
    if driver.find_elements("class name","css-1wc0q5e"):
        print("COOKIE ISSUE SOLVING")
        driver.find_element("class name","css-1wc0q5e").click()

    time.sleep(api_delay_term)

    if statistic !="summary":

        button = driver.find_element("xpath", button_xpath)

        driver.execute_script("arguments[0].click();", button);
        ## print resultant page title
        # print("Page title is: ")
        # print(driver.title)

        time.sleep(api_delay_term)

    return driver

def remove_nan_values_added_while_scrapping(df):
    """
    This takes a dataframe that might be faulty after the scrapping with a lot of nan values and removes the 

    Args:
        df : Dataframe with faulty rows

    return: 
        df: Modified dataframe without a nan rows 
    """

    print('Removing Nan Added Rows')

    df.to_csv("for_fix.csv")
    df = pd.read_csv("for_fix.csv")
    df = df.dropna().reset_index(drop=True)
    os.remove("for_fix.csv")

    return df

def get_start_and_sub_games(element):
    """
        Separate start_number_of_game (sub_number_of_game) intro start_number_of_game and sub_number_of_game
    """
    games = element.find_elements("css selector","td")[4].text

    parts = games.split("(")
    if(len(parts)==2):
        start_games = parts[0]
        sub_games = parts[1].replace(')','')
    else:
        start_games = games
        sub_games = 0
    return start_games, sub_games

def crawl_player_team_stats_summary(url):
    """
    Crawling summary statistics of certain team
    
    Args :
        url : URL to Scrape  
        
    return :
        player summary statistics (dataframe)
    
    """
    driver = establish_driver_connection(url)
    
    # make pandas dataframe     
    player_summary_df = pd.DataFrame(columns=[
        "player_number", "name", "age", "position", "tall", "weight", "games", "start_games", "sub_games", "mins", 
        "goals", "assists", "yellow_cards", "red_cards", 
        "shots_per_game", "pass_success_percentage", "aerials_won_per_game", "man_of_the_match", 
        "rating"
        ])
    
    # get player summay datas
    #elements = driver.find_elements_by_css_selector("#player-table-statistics-body tr")
    elements = driver.find_elements("css selector","#player-table-statistics-body tr") 

    print('Fetching Player Table')

    for element in elements:
        
        start_games,sub_games = get_start_and_sub_games(element)
        
        player_dict = { 
            "player_number": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].get_attribute("href").split("/")[4],
            "name": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].find_elements("css selector","span")[0].text,
            "age": element.find_elements("class name","player-meta-data")[0].text,
            "position": element.find_elements("class name","player-meta-data")[1].text[1:],
            "tall": element.find_elements("css selector","td")[2].text,
            "weight": element.find_elements("css selector","td")[3].text,
            "games": element.find_elements("css selector","td")[4].text,
            "start_games": start_games,
            "sub_games": sub_games,
            "mins": element.find_elements("css selector","td")[5].text,

            "goals": element.find_elements("css selector","td")[6].text,
            "assists": element.find_elements("css selector","td")[7].text,
            "yellow_cards": element.find_elements("css selector","td")[8].text,
            "red_cards": element.find_elements("css selector","td")[9].text,
            "shots_per_game": element.find_elements("css selector","td")[10].text,
            "pass_success_percentage": element.find_elements("css selector","td")[11].text,
            "aerials_won_per_game": element.find_elements("css selector","td")[12].text,
            "man_of_the_match": element.find_elements("css selector","td")[13].text, 
            "rating": element.find_elements("css selector","td")[14].text,  
        }

        #print(f'Populating CSV with {player_dict}')
        player_summary_df.loc[len(player_summary_df)] = player_dict
       
    # close webdriver
    print('Close Webdriver')
    driver.close()

    # Replace - with 0 among stats
    player_summary_df = replace_pd(player_summary_df)
    # Remove NaN values rows
    player_summary_df = remove_nan_values_added_while_scrapping(player_summary_df)

    return player_summary_df

def crawl_player_team_stats_offensive(url, is_current_season = False):

    if(is_current_season):
        driver = establish_driver_connection(url, 'offensive', '//a[contains(@href,"#team-squad-stats-offensive")]')
    else:    
        driver = establish_driver_connection(url, 'offensive', '//a[contains(@href,"#team-squad-archive-stats-offensive")]')
    
    # make pandas dataframe
    player_offensive_df = pd.DataFrame(columns = [ 
        "player_number", "name", "age", "position", "tall", "weight", "games", "start_games", "sub_games", "mins", 
        "goals", "assists", "shot_per_game", "key_passes_per_game", "dribbles_per_game",
        "fouled_per_game", "offsides_per_game", "dispossessed_per_game", "bad_control_per_game", 
        "rating"
        ])

    
    elements = driver.find_elements("css selector","#player-table-statistics-body tr") 
    print(f"Number of Elements {len(elements)}")

    print('Fetching Player Table')

    for element in elements:
        #print(f' Size of an element {len(element.find_elements("css selector","td"))}')
        if(len(element.find_elements("css selector","td")) < 16): continue 

        start_games,sub_games = get_start_and_sub_games(element)

        #print(f' Rating {element.find_elements("css selector","td")[15].text}')
        
        player_dict = { 
            "player_number": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].get_attribute("href").split("/")[4],
            "name": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].find_elements("css selector","span")[0].text,
            "age": element.find_elements("class name","player-meta-data")[0].text,
            "position": element.find_elements("class name","player-meta-data")[1].text[1:],
            "tall": element.find_elements("css selector","td")[2].text,
            "weight": element.find_elements("css selector","td")[3].text,
            "games": element.find_elements("css selector","td")[4].text,
            "start_games": start_games,
            "sub_games": sub_games,
            "mins": element.find_elements("css selector","td")[5].text,

            "goals": element.find_elements("css selector","td")[6].text,
            "assists": element.find_elements("css selector","td")[7].text,
            "shot_per_game": element.find_elements("css selector","td")[8].text,
            "key_passes_per_game": element.find_elements("css selector","td")[9].text,
            "dribbles_per_game": element.find_elements("css selector","td")[10].text,
            "fouled_per_game": element.find_elements("css selector","td")[11].text,
            "offsides_per_game": element.find_elements("css selector","td")[12].text,
            "dispossessed_per_game": element.find_elements("css selector","td")[13].text,
            "bad_control_per_game": element.find_elements("css selector","td")[14].text,
            "rating": element.find_elements("css selector","td")[15].text,
        }

        #print(f'Populating CSV with {player_dict}')
        player_offensive_df.loc[len(player_offensive_df)] = player_dict

    print('Close Webdriver')
    driver.close()
    
    # Replace - with 0 among stats
    player_offensive_df = replace_pd(player_offensive_df)
    # Remove NaN values rows
    player_offensive_df = remove_nan_values_added_while_scrapping(player_offensive_df)

    return player_offensive_df

def crawl_player_team_stats_defensive(url, is_current_season = False):
    if is_current_season:
        driver = establish_driver_connection(url, 'defensive', '//a[contains(@href,"#team-squad-stats-defensive")]')
    else:
        driver = establish_driver_connection(url, 'defensive', '//a[contains(@href,"#team-squad-archive-stats-defensive")]')

    # make pandas dataframe
    player_defensive_df = pd.DataFrame(columns = [ 
        "player_number", "name", "age", "position", "tall", "weight", "games", "start_games", "sub_games", "mins", 
        "tackles_per_game", "interceptions_per_game", 
        "fouls_per_game", "offsides_won_per_game",
        "clearances_per_game", "dribbled_past_per_game", 
        "outfielder_blocks_per_game", "own_goals",
        "rating"
        ])

    elements = driver.find_elements("css selector","#player-table-statistics-body tr") 
    #print(f"Number of Elements {len(elements)}")

    print('Fetching Player Table')

    for element in elements:
        if(len(element.find_elements("css selector","td")) < 15): continue 

        start_games,sub_games = get_start_and_sub_games(element)    
        
        player_dict = { 
            "player_number": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].get_attribute("href").split("/")[4],
            "name": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].find_elements("css selector","span")[0].text,
            "age": element.find_elements("class name","player-meta-data")[0].text,
            "position": element.find_elements("class name","player-meta-data")[1].text[1:],
            "tall": element.find_elements("css selector","td")[2].text,
            "weight": element.find_elements("css selector","td")[3].text,
            "games": element.find_elements("css selector","td")[4].text,
            "start_games": start_games,
            "sub_games": sub_games,
            "mins": element.find_elements("css selector","td")[5].text,
            "tackles_per_game": element.find_elements("css selector","td")[6].text,
            "interceptions_per_game": element.find_elements("css selector","td")[7].text,
            "fouls_per_game": element.find_elements("css selector","td")[8].text,
            "offsides_won_per_game": element.find_elements("css selector","td")[9].text,
            "clearances_per_game": element.find_elements("css selector","td")[10].text,
            "dribbled_past_per_game": element.find_elements("css selector","td")[11].text,
            "outfielder_blocks_per_game": element.find_elements("css selector","td")[12].text,
            "own_goals": element.find_elements("css selector","td")[13].text,
            "rating": element.find_elements("css selector","td")[14].text,
        }

        #print(f'Populating CSV with {player_dict}')
        player_defensive_df.loc[len(player_defensive_df)] = player_dict

    print('Close Webdriver')
    driver.close()

    # Replace - with 0 among stats
    player_defensive_df = replace_pd(player_defensive_df)
    # Remove NaN values rows
    player_defensive_df = remove_nan_values_added_while_scrapping(player_defensive_df)

    return player_defensive_df

def crawl_player_team_stats_passing(url, is_current_season = False):
    if is_current_season:
        driver = establish_driver_connection(url, 'passing', '//a[contains(@href,"#team-squad-stats-passing")]')
    else:
        driver = establish_driver_connection(url, 'passing', '//a[contains(@href,"#team-squad-archive-stats-passing")]')

    # make pandas dataframe
    player_passing_df = pd.DataFrame(columns = [ 
        "player_number", "name", "age", "position", "tall", "weight", "games", "start_games", "sub_games", "mins", 
        "total_assists", "key_passes_per_game", "passes_per_game",
        "pass_success_percentage", "crosses_per_game", "long_ball_per_game", "through_balls_per_game", 
        "rating"
        ])

    elements = driver.find_elements("css selector","#player-table-statistics-body tr") 
    #print(f"Number of Elements {len(elements)}")

    print('Fetching Player Table')

    for element in elements:
        if(len(element.find_elements("css selector","td")) < 14): continue 

        start_games,sub_games = get_start_and_sub_games(element)
        
        player_dict = { 
            "player_number": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].get_attribute("href").split("/")[4],
            "name": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].find_elements("css selector","span")[0].text,
            "age": element.find_elements("class name","player-meta-data")[0].text,
            "position": element.find_elements("class name","player-meta-data")[1].text[1:],
            "tall": element.find_elements("css selector","td")[2].text,
            "weight": element.find_elements("css selector","td")[3].text,
            "games": element.find_elements("css selector","td")[4].text,
            "start_games": start_games,
            "sub_games": sub_games,
            
            "mins": element.find_elements("css selector","td")[5].text,
            "total_assists": element.find_elements("css selector","td")[6].text,
            "key_passes_per_game": element.find_elements("css selector","td")[7].text,
            "passes_per_game": element.find_elements("css selector","td")[8].text, 
            "pass_success_percentage": element.find_elements("css selector","td")[9].text, 
            "crosses_per_game": element.find_elements("css selector","td")[10].text, 
            "long_ball_per_game": element.find_elements("css selector","td")[11].text,
            "through_balls_per_game": element.find_elements("css selector","td")[12].text, 
            
            "rating": element.find_elements("css selector","td")[13].text,
        }

        #print(f'Populating CSV with {player_dict}')
        player_passing_df.loc[len(player_passing_df)] = player_dict

    print('Close Webdriver')
    driver.close()

    # Replace - with 0 among stats
    player_passing_df = replace_pd(player_passing_df)
    # Remove Nan value rows
    player_passing_df = remove_nan_values_added_while_scrapping(player_passing_df)

    return player_passing_df


def establish_driver_connection_for_detailed_section(url, xpath_for_current_or_archive, stats_selection = "Shots", is_circumstance_needed = True, circumstance_selection_text = 'Zones', stats_period_selection = 'Total', api_delay_term = 5):
    driver = establish_driver_connection(url, 'detailed', xpath_for_current_or_archive)

    select = Select(driver.find_element("id","category"))

    # Tackles, Interceptions, Fouls, Cards, Offsides, Clearances, Blocks, Saves
    # Shots, Goals, Dribbles, Possession Lost, Aerial
    # Passes, Key Passes, Assists
    print(f"Stats Option {stats_selection}")
    select.select_by_visible_text(stats_selection)
    time.sleep(api_delay_term)

    # Zones, Situations, Accuracy, Body Part
    if is_circumstance_needed:
        print(f"Circumstance Option {circumstance_selection_text}")
        select = Select(driver.find_element("id","subcategory"))
        select.select_by_visible_text(circumstance_selection_text)
    time.sleep(api_delay_term)


    select = Select(driver.find_element("id","statsAccumulationType"))

    print(f"Stats Period {stats_period_selection}")
    # Total, Per game, Per 90 minutes, Total
    select.select_by_visible_text(stats_period_selection)
    time.sleep(api_delay_term)


    return driver 


def create_crawler_empty_df(list_of_extra_columns, are_sub_games_existent = False):

    list_of_columns =["player_number", "name", "age", "position", "tall", "weight", "games"]
    list_of_columns.extend(["start_games", "sub_games", "mins"] if are_sub_games_existent else ["mins"]) 
    
    list_of_columns.extend(list_of_extra_columns)
    list_of_columns.append('rating')

    #print(list_of_columns)

    empty_df = pd.DataFrame(columns = list_of_columns)
    #print(empty_df)

    return empty_df


def create_dictionary_row_for_crawler(element, list_of_extra_entries, are_sub_games_existent = False):
    player_dict = { 
            "player_number": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].get_attribute("href").split("/")[4],
            "name": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].find_elements("css selector","span")[0].text,
            "age": element.find_elements("class name","player-meta-data")[0].text,
            "position": element.find_elements("class name","player-meta-data")[1].text[1:],
            "tall": element.find_elements("css selector","td")[2].text,
            "weight": element.find_elements("css selector","td")[3].text,
            "games": element.find_elements("css selector","td")[4].text,
    }
    
    if are_sub_games_existent:
        start_games,sub_games = get_start_and_sub_games(element)
        player_dict["start_games"] = start_games
        player_dict["sub_games"] = sub_games
    
    player_dict["mins"] = element.find_elements("css selector","td")[5].text 
    
    table_data_index = 6
    for entry in list_of_extra_entries:
        player_dict[entry] = element.find_elements("css selector","td")[table_data_index].text 
        table_data_index += 1

    player_dict["rating"] = element.find_elements("css selector","td")[table_data_index].text
    print(player_dict)

    return player_dict


def crawl_player_team_stats_detailed_shots_zones(url, is_current_season = False):
    if is_current_season:
        driver = establish_driver_connection_for_detailed_section(url, '//a[contains(@href,"#team-squad-stats-detailed")]')
    else:
        driver = establish_driver_connection_for_detailed_section(url, '//a[contains(@href,"#team-squad-archive-stats-detailed")]')

     # make pandas dataframe

    player_detailed_shots_zones_df =  create_crawler_empty_df(["total_shots_per_game", "outside_the_penalty_area_shots_per_game", "six_yard_box_shots_per_game", "penalty_area_shots_per_game"], are_sub_games_existent = False)
    # player_detailed_shots_zones_df = pd.DataFrame(columns = [ 
    #     "player_number", "name", "age", "position", "tall", "weight", "games", "mins",

    #     "total_shots_per_game", "outside_the_penalty_area_shots_per_game", "six_yard_box_shots_per_game", "penalty_area_shots_per_game",

    #     "rating"
    #     ])

    elements = driver.find_elements("css selector","#player-table-statistics-body tr") 
    #print(f"Number of Elements {len(elements)}")

    print('Fetching Player Table')

    for element in elements:
        if(len(element.find_elements("css selector","td")) >11): continue 
        #print(f'Name {element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].find_elements("css selector","span")[0].text}  CELLS {len(element.find_elements("css selector","td"))}')
        

        player_dict = create_dictionary_row_for_crawler(element, ["total_shots_per_game", "outside_the_penalty_area_shots_per_game", "six_yard_box_shots_per_game", "penalty_area_shots_per_game"], False)

        # player_dict = { 
        #     "player_number": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].get_attribute("href").split("/")[4],
        #     "name": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].find_elements("css selector","span")[0].text,
        #     "age": element.find_elements("class name","player-meta-data")[0].text,
        #     "position": element.find_elements("class name","player-meta-data")[1].text[1:],
        #     "tall": element.find_elements("css selector","td")[2].text,
        #     "weight": element.find_elements("css selector","td")[3].text,
        #     "games": element.find_elements("css selector","td")[4].text,
        #     "mins": element.find_elements("css selector","td")[5].text,

        #     "total_shots_per_game": element.find_elements("css selector","td")[6].text,
        #     "outside_the_penalty_area_shots_per_game": element.find_elements("css selector","td")[7].text,
        #     "six_yard_box_shots_per_game": element.find_elements("css selector","td")[8].text, 
        #     "penalty_area_shots_per_game": element.find_elements("css selector","td")[9].text,

        #     "rating": element.find_elements("css selector","td")[10].text,
        # }

        # print(f'Populating CSV with {player_dict}')
        player_detailed_shots_zones_df.loc[len(player_detailed_shots_zones_df)] = player_dict

    print('Close Webdriver')
    driver.close()

    # Replace - with 0 among stats
    player_detailed_shots_zones_df = replace_pd(player_detailed_shots_zones_df)
    # Remove Nan value rows
    player_detailed_shots_zones_df = remove_nan_values_added_while_scrapping(player_detailed_shots_zones_df)

    return player_detailed_shots_zones_df  

def crawl_player_team_stats_detailed_shots_situation(url, is_current_season = False):
    if is_current_season:
        driver = establish_driver_connection_for_detailed_section(url, '//a[contains(@href,"#team-squad-stats-detailed")]',"Situations")
    else:
        driver = establish_driver_connection_for_detailed_section(url, '//a[contains(@href,"#team-squad-archive-stats-detailed")]', "Situations")

     # make pandas dataframe
    player_detailed_shots_situation_df =  create_crawler_empty_df(["total_shots_per_game", "shots_from_open_play_per_game", "shots_from_counters_play_per_game", "shots_from_set_pieces_play_per_game", "penalties_taken_per_game"], are_sub_games_existent = False)
    
    # player_detailed_shots_selection_df = pd.DataFrame(columns = [ 
    #     "player_number", "name", "age", "position", "tall", "weight", "games", "mins",

    #     "total_shots_per_game", "outside_the_penalty_area_shots_per_game", "six_yard_box_shots_per_game", "penalty_area_shots_per_game",

    #     "rating"
    #     ])
    print(player_detailed_shots_situation_df)




def correction_of_all_dataframes(statistic = 'summary'):
    '''
        Used to correct any type of statistical dataframes from whoscored
    '''
    for league, team_details in whoscored_teams_dict.items():
        # paths = []
        print(f'LEAGUE {league}')
        for year in range(2009,2023):
            print(f'Year {year}')
            path =f'dataframes/whoscored_player_{statistic}_stats/{league}/season_{year}_{year+1}'
            filenames = next(walk(path), (None, None, []))[2]
            filenames = [f'{path}/{filename}' for filename in filenames]

            print(filenames)
            for file_name in filenames:
                print(f'File {file_name}')
                csv = pd.read_csv(file_name)

                # Correction
                csv.rename(columns = {'yel':'yellow_cards','red':'red_cards','spg':'shots_per_game','ps':'pass_success_percentage','aw':'aerials_won','motm':'man_of_the_match'}, inplace=True)
                csv.drop(['Unnamed: 0'], axis = 1)
                column_names =["player_number","name","age","position","tall","weight","games","start_games","sub_games","mins","goals","assists","yellow_cards","red_cards","shots_per_game","pass_success_percentage","aerials_won","man_of_the_match","rating"]
                csv = csv.reindex(columns = column_names)
                # End of Correction

                #csv = replace_pd(csv)

                csv.to_csv(file_name)
                

if __name__ == "__main__":

    establish_driver_connection_for_detailed_section('https://www.whoscored.com/Teams/65','//a[contains(@href,"#team-squad-stats-detailed")]', "Goals", True,"Situations", "Per 90 mins", 5)
    

    # print(csv.head(5))
    # Test crawler
    #("https://www.whoscored.com/Teams/65/Archive/?stageID=19895", False)
    #("https://www.whoscored.com/Teams/65", True)

    df = crawl_player_team_stats_detailed_shots_situation("https://www.whoscored.com/Teams/65", True)
    #df = crawl_player_team_stats_detailed_shots_zones("https://www.whoscored.com/Teams/65/Archive/?stageID=19895", False)

    #df.to_csv("test_result.csv")

    # pd = crawl_player_team_stats_summary("https://www.whoscored.com/Teams/13/Archive")
    # pd.to_csv("test_results.csv")

    # What to modify for each type of statistic


    # put instead of stat offensive, deffensive, passing and detailed_zones_shots last one in Progress
    # for league, teams_details in whoscored_teams_dict.items():
    #     print(league, '->', teams_details)
    #     crawl_chosen_stats_between_years(league, teams_details, 2009, 2023, stat = "detailed_zones_shots")


    # Correction already modified in code
    # correction_of_all_dataframes('summary')
                
    

