from operator import is_
from re import X
from constants import whoscored_teams_dict, whoscored_detailed_options, who_scored_simple_columns, API_DELAY_FOR_YOUR_PC

import time
import pandas as pd
pd.set_option('display.max_columns', None) 
pd.options.mode.chained_assignment = None

import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.safari 
from selenium import webdriver
from selenium.webdriver.support.select import Select

#for stale element reference
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from empty_folder_creator import create_empty_directories
from os import stat, walk
import os 

# used to map time of operations
import time
import logging
logger = logging.getLogger('my_module_name')

driver_connection_counter = 0
driver_connection_time_sum = 0
driver_connection_time_average = 0

fetching_data_counter = 0
fetching_data_time_sum = 0
fetching_data_time_average = 0

def replace_pd(df):
    # start process    
    now = time.time()

    mapping = {'-': 0} 
    replace_dict = {}
    for colum in df.columns:
        replace_dict[colum] = mapping
    
    # end of the process
    later = time.time()
    # compute process time
    difference = float(later - now)

    print(f"[TIME LOG 4] - Replace - with 0 took {difference} seconds")
    logging.info(f"[TIME LOG 4] - Replace - with 0 took {difference} seconds")

    return df.replace(replace_dict)

def save_stats_csv(df, stat, league, team, season_start_year):
    print('Saving CSV to File')
    team = team.replace(' ','_')
    filename = f'dataframes/whoscored_player_{stat}_stats/{league}/season_{season_start_year}_{season_start_year+1}/{team}_{stat}_stats_in_season_{season_start_year}_{season_start_year+1}.csv'
    
    print(f'FILENAME {filename}')
    df.to_csv(filename)

def crawl_chosen_stats_between_years(league, teams_details, start_year, end_year, stat='summary'):
    # start of the whole process
    global driver_connection_counter, driver_connection_time_sum, driver_connection_time_average
    global fetching_data_counter, fetching_data_time_sum, fetching_data_time_average

    now_total = time.time()
    logging.basicConfig(filename = f'debugger_logs/debugger_time_crawling_for_{stat}.log', encoding='utf-8', level=logging.INFO, filemode = 'a')

    create_empty_directories('dataframes', f'whoscored_player_{stat}_stats', league, start_year, end_year, True)

    for team, code in teams_details.items():       
        dict_of_league_urls = crawl_all_urls_for_given_team_in_league_competitions(code, league, first_season_year = start_year, last_season_year = end_year)
        
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
                case 'detailed_offensive':
                    df_detailed_offensive = crawl_player_team_stats_detailed(item[1], "offensive", is_current_season)
                    is_current_season = False

                    save_stats_csv(df_detailed_offensive,'detailed_offensive',league, team, season_start_year = int(item[0].split('_')[1]))                
                case 'detailed_defensive':
                    df_detailed_defensive = crawl_player_team_stats_detailed(item[1], "defensive", is_current_season)
                    is_current_season = False

                    save_stats_csv(df_detailed_defensive,'detailed_defensive',league, team, season_start_year = int(item[0].split('_')[1]))                
                case 'detailed_passing':
                    df_detailed_passing = crawl_player_team_stats_detailed(item[1], "passing", is_current_season)
                    is_current_season = False

                    save_stats_csv(df_detailed_passing,'detailed_passing',league, team, season_start_year = int(item[0].split('_')[1]))                
                      
                case _:
                    #To Be Implemented
                    print('nada')

    # end of the whole process
    later_total = time.time()
    # compute the whole process time
    difference_total = float(later_total - now_total)

    driver_connection_time_average += float(driver_connection_time_sum) / float(driver_connection_counter)
    fetching_data_time_average += float(fetching_data_time_sum) / float(fetching_data_counter)

    print(f"[TIME LOG DRIVER CONNECTION Average Time for {stat.upper()} in league {league.upper()}] - On Average the Process for league {league} took {float(driver_connection_time_sum) / float(driver_connection_counter)} seconds per team")
    logging.info(f"[TIME LOG DRIVER CONNECTION Average Time for {stat.upper()} in league {league.upper()}] - On Average the Process for league {league} took {float(driver_connection_time_sum) / float(driver_connection_counter)} seconds per team")
    
    print(f"[TIME LOG FETCHING DATA Average Time for {stat.upper()} in league {league.upper()}] - On Average the Process for league {league} took {float(fetching_data_time_sum) / float(fetching_data_counter)} seconds per team")
    logging.info(f"[TIME LOG FETCHING DATA Average Time for {stat.upper()} in league {league.upper()}] - On Average the Process for league {league} took {float(fetching_data_time_sum) / float(fetching_data_counter)} seconds per team")

    print(f"[TIME LOG FINAL Crawling for {stat.upper()} for league {league.upper()}] - Whole Process took for league {league} took {difference_total} seconds")
    logging.info(f"[TIME LOG FINAL Crawling for {stat.upper()} for league {league.upper()}] - Whole Process took for league {league} took {difference_total} seconds")   


def transform_competition_name(competition_name):
    match competition_name:
        case 'epl':
            competition_text = 'Premier League'
            season_text_start = 'epl'
        case 'bundesliga':
            competition_text = 'Bundesliga'
            season_text_start = 'bundesliga'
        case 'la liga':
            competition_text = 'LaLiga'
            season_text_start = 'la liga'
        case 'ligue 1':
            competition_text = 'Ligue 1'
            season_text_start = 'ligue 1'
        case 'serie a':
            competition_text = 'Serie A'
            season_text_start = 'seria a'
        case _:
            competition_text = 'Champions League'
            season_text_start = 'champions league'

    return competition_text,season_text_start

def crawl_all_urls_for_given_team_in_league_competitions(team_id, competition_name, first_season_year = 2009, last_season_year = 2023):
    # start of the process  
    now = time.time()
    dict_of_league_competitions_urls = dict()

    if last_season_year > 2023:
        last_season_year = 2023
    if last_season_year == 2023:
        last_season_year -= 1
        url_current_season = f'https://www.whoscored.com/Teams/{team_id}'
        dict_of_league_competitions_urls[f'{competition_name}_{last_season_year}_{last_season_year+1}'] = url_current_season



    url = f'https://www.whoscored.com/Teams/{team_id}/Archive'
    


    driver = webdriver.Chrome(executable_path = 'exe_dependencies/chromedriver')
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

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
            end_year = season_full.split('/')[1]
            season_text = f'{start_year}_{end_year}'
            season_text = f'{season_text_start}_{season_text}'
            #print(season_text)
            if int(start_year) >= first_season_year:
                if int(end_year)<= last_season_year:
                    url_to_append = f'https://www.whoscored.com/Teams/{team_id}/Archive/?stageId={value}'
                    dict_of_league_competitions_urls[season_text] = url_to_append

   # print("DICT COMPETITIONS URLS:")
    #print(dict_of_league_competitions_urls)
    # end of the process
    later = time.time()
    difference = float(later - now)

    print(f"[TIME LOG CRAWL URL] - Crawling All URLS took {difference} seconds")
    logging.info(f"[TIME LOG CRAWL URL] - Crawling All URLS took {difference} seconds")    
    
    return dict_of_league_competitions_urls
    

driver_installed_singleton = None
def establish_driver_connection(url, statistic = 'summary', button_xpath = '//a[contains(@href,"#team-squad-archive-stats-offensive")]', api_delay_term = API_DELAY_FOR_YOUR_PC):
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
    global driver_installed_singleton, driver_connection_counter, driver_connection_time_sum
    # NEVER EVER Try open Chrome Silently
    # THEY WILL BAN YOU 
    #CHROME_PATH = '/Applications/Google Chrome.app'
    #CHROMEDRIVER_PATH = '/exe_dependencies/chromedriver.exe'
    # WINDOW_SIZE = "1920,1080"

    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    #chrome_options.binary_location = CHROME_PATH

    #driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), chrome_options = chrome_options)
    # Classical
    # start of the process
    now = time.time()

    #driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
    #driver = webdriver.Chrome(service = Service(ChromeDriverManager(os_type = "mac64_m1").install()))
    
    driver = webdriver.Chrome(executable_path = 'exe_dependencies/chromedriver')
    # if driver_installed_singleton == None: 
    #     driver_installed_singleton = webdriver.Chrome(executable_path = 'exe_dependencies/chromedriver')
    # driver = driver_installed_singleton

    #driver = webdriver.Chrome(ChromeDriverManager().install())
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
    
    # end of the process
    later = time.time()
    # compute process time
    difference = float(later - now)

    print(f"[TIME LOG 1] - Establishing Driver Connection took {difference} seconds")
    logging.info(f"[TIME LOG 1] - Establishing Driver Connection took {difference} seconds")

    driver_connection_counter += 1
    driver_connection_time_sum += difference

    return driver

def remove_nan_values_added_while_scrapping(df):
    """
    This takes a dataframe that might be faulty after the scrapping with a lot of nan values and removes the 

    Args:
        df : Dataframe with faulty rows

    return: 
        df: Modified dataframe without a nan rows 
    """
    # start process    
    now = time.time()

    print('Removing Nan Added Rows')

    df.to_csv("for_fix.csv")
    df = pd.read_csv("for_fix.csv")
    df = df.dropna().reset_index(drop=True)
    os.remove("for_fix.csv")

    # end of the process
    later = time.time()
    # compute process time
    difference = float(later - now)

    print(f"[TIME LOG 5] - Remove Nan rows took {difference} seconds")
    logging.info(f"[TIME LOG 5] - Remove Nan rows took {difference} seconds")

    return df

def get_start_and_sub_games(element):
    """
        Separate start_number_of_game (sub_number_of_game) intro start_number_of_game and sub_number_of_game
    """
    #start of the process
    #now = time.time()

    games = element.find_elements("css selector","td")[4].text

    parts = games.split("(")
    if(len(parts)==2):
        start_games = parts[0]
        sub_games = parts[1].replace(')','')
    else:
        start_games = games
        sub_games = 0

    #end of the process
    #later = time.time()
    #compute process time
    #difference = float(later - now)

    #print(f"[TIME LOG 4] - Creating Get {difference} seconds")
    #logging.info(f"[TIME LOG 4] - Creating Get {difference} seconds")

    return start_games, sub_games

def create_crawler_empty_df(list_of_extra_columns, are_sub_games_existent = False):
    # start of the process
    now = time.time()

    list_of_columns =["player_number", "name", "age", "position", "tall", "weight", "games"]
    list_of_columns.extend(["start_games", "sub_games", "mins"] if are_sub_games_existent else ["mins"]) 
    
    list_of_columns.extend(list_of_extra_columns)
    list_of_columns.append('rating')

    #print(list_of_columns)

    empty_df = pd.DataFrame(columns = list_of_columns)
    #print(empty_df)

    # end of the process
    later = time.time()
    # compute process time
    difference = float(later - now)

    print(f"[TIME LOG 2] - Creating Empty Dataframe took {difference} seconds")
    logging.info(f"[TIME LOG 2] - Creating Empty Dataframe took {difference} seconds")

    return empty_df

def create_dictionary_row_for_crawler(element, list_of_extra_columns, are_sub_games_existent = False):
    #start of the process
    #now = time.time()

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
    for entry in list_of_extra_columns:
        player_dict[entry] = element.find_elements("css selector","td")[table_data_index].text 
        table_data_index += 1

    player_dict["rating"] = element.find_elements("css selector","td")[table_data_index].text
    #print(player_dict)
    
    #end of the process
    #later = time.time()
    #compute process time
    #difference = int(later - now)

    #print(f"[TIME LOG 3] - Creating Player Dictionary took {difference} seconds")
    #logging.info(f"[TIME LOG 3] - Creating Player Dictionary took {difference} seconds")

    return player_dict

def crawl_player_team_stats_summary(url):
    """
    Crawling summary statistics of certain team
    
    Args :
        url : URL to Scrape  
        
    return :
        player summary statistics (dataframe)
    
    """
    # start of all process
    now_total = time.time()
    
    logging.basicConfig(filename='debugger_logs/debugger_time_summary.log', encoding='utf-8', level=logging.INFO, filemode="a")

    driver = establish_driver_connection(url)
    
    player_summary_df =  create_crawler_empty_df(list_of_extra_columns = who_scored_simple_columns['summary'], are_sub_games_existent = True)

    elements = driver.find_elements("css selector","#player-table-statistics-body tr") 

    print('Fetching Player Table')

    # start process    
    now = time.time()

    for element in elements:
        player_dict = create_dictionary_row_for_crawler(element, list_of_extra_columns = who_scored_simple_columns['summary'], are_sub_games_existent = True)
        
        player_summary_df.loc[len(player_summary_df)] = player_dict

    # end of the process
    later = time.time()
    # compute process time
    difference = float(later - now)

    print(f"[TIME LOG 3 SUMMARY] - Fetching Player Data took {difference} seconds")
    logging.info(f"[TIME LOG 3 SUMMARY] - Fetching Player Data took {difference} seconds")    

    # close webdriver
    print('Close Webdriver')
    driver.close()

    # Replace - with 0 among stats
    player_summary_df = replace_pd(player_summary_df)
    # Remove NaN values rows
    player_summary_df = remove_nan_values_added_while_scrapping(player_summary_df)

    # end of the whole process
    later_total = time.time()
    # compute time of the whole process time
    difference_total = float(later_total - now_total)

    print(f"[TIME LOG FINAL SUMMARY] - Whole Process took {difference_total} seconds")
    logging.info(f"[TIME LOG FINAL SUMMARY] - Whole Process took {difference_total} seconds")    

    print("[LOG SUMMARY] - Summary Fetching Done")
    logging.info("[LOG SUMMARY] - Summary Fetching Done")  


    return player_summary_df

def crawl_player_team_stats_offensive(url, is_current_season = False):
    # start of the whole process
    now_total = time.time()
    logging.basicConfig(filename='debugger_logs/debugger_time_offensive.log', encoding='utf-8', level=logging.INFO, filemode = 'a')

    if(is_current_season):
        driver = establish_driver_connection(url, 'offensive', '//a[contains(@href,"#team-squad-stats-offensive")]')
    else:    
        driver = establish_driver_connection(url, 'offensive', '//a[contains(@href,"#team-squad-archive-stats-offensive")]')
    
    player_offensive_df =  create_crawler_empty_df(list_of_extra_columns = who_scored_simple_columns['offensive'], are_sub_games_existent = True)

    
    elements = driver.find_elements("css selector","#player-table-statistics-body tr") 
    print(f"Number of Elements {len(elements)}")

    print('Fetching Player Table')

    # start process    
    now = time.time()

    for element in elements:
        if(len(element.find_elements("css selector","td")) < 16): continue 

        player_dict = create_dictionary_row_for_crawler(element, list_of_extra_columns = who_scored_simple_columns['offensive'], are_sub_games_existent = True)

        player_offensive_df.loc[len(player_offensive_df)] = player_dict
    # end of the process
    later = time.time()
    # compute process time
    difference = float(later - now)

    print(f"[TIME LOG 3 OFFENSIVE] - Fetching Player Data took {difference} seconds")
    logging.info(f"[TIME LOG 3 OFFENSIVE] - Fetching Player Data took {difference} seconds")    
    
    print('Close Webdriver')
    driver.close()
    
    # Replace - with 0 among stats
    player_offensive_df = replace_pd(player_offensive_df)
    # Remove NaN values rows
    player_offensive_df = remove_nan_values_added_while_scrapping(player_offensive_df)

    # end of the whole process
    later_total = time.time()
    # compute the whole process time
    difference_total = float(later_total - now_total)

    print(f"[TIME LOG FINAL OFFENSIVE] - Whole Process took {difference_total} seconds")
    logging.info(f"[TIME LOG FINAL OFFENSIVE] - Whole Process took {difference_total} seconds") 

    print("[LOG OFFENSIVE] - Offensive Fetching Done")
    logging.info("[LOG OFFENSIVE] - Offensive Fetching Done") 

    return player_offensive_df

def crawl_player_team_stats_defensive(url, is_current_season = False):
    # start of the whole process
    now_total = time.time()
    logging.basicConfig(filename='debugger_logs/debugger_time_defensive.log', encoding='utf-8', level=logging.INFO, filemode = 'a')

    if is_current_season:
        driver = establish_driver_connection(url, 'defensive', '//a[contains(@href,"#team-squad-stats-defensive")]')
    else:
        driver = establish_driver_connection(url, 'defensive', '//a[contains(@href,"#team-squad-archive-stats-defensive")]')
    
    player_defensive_df =  create_crawler_empty_df(list_of_extra_columns = who_scored_simple_columns['defensive'], are_sub_games_existent = True)

    elements = driver.find_elements("css selector","#player-table-statistics-body tr") 

    print('Fetching Player Table')

    # start process    
    now = time.time()

    for element in elements:
        if(len(element.find_elements("css selector","td")) < 15): continue 

        
        player_dict = create_dictionary_row_for_crawler(element, list_of_extra_columns = who_scored_simple_columns['defensive'], are_sub_games_existent = True)

        player_defensive_df.loc[len(player_defensive_df)] = player_dict

    # end of the process
    later = time.time()
    # compute process time
    difference = float(later - now)

    print(f"[TIME LOG 3 DEFENSIVE] - Fetching Player Data took {difference} seconds")
    logging.info(f"[TIME LOG 3 DEFENSIVE] - Fetching Player Data took {difference} seconds")    
    
    print('Close Webdriver')
    driver.close()
    

    # Replace - with 0 among stats
    player_defensive_df = replace_pd(player_defensive_df)
    # Remove NaN values rows
    player_defensive_df = remove_nan_values_added_while_scrapping(player_defensive_df)

    # end of the whole process
    later_total = time.time()
    # compute the whole process time
    difference_total = float(later_total - now_total)

    print(f"[TIME LOG FINAL OFFENSIVE] - Whole Process took {difference_total} seconds")
    logging.info(f"[TIME LOG FINAL OFFENSIVE] - Whole Process took {difference_total} seconds") 

    print("[LOG OFFENSIVE] - Offensive Fetching Done")
    logging.info("[LOG OFFENSIVE] - Offensive Fetching Done") 

    return player_defensive_df

def crawl_player_team_stats_passing(url, is_current_season = False):    
    # start of the whole process
    now_total = time.time()
    logging.basicConfig(filename='debugger_logs/debugger_time_passing.log', encoding='utf-8', level=logging.INFO, filemode = 'a')
        
    if is_current_season:
        driver = establish_driver_connection(url, 'passing', '//a[contains(@href,"#team-squad-stats-passing")]')
    else:
        driver = establish_driver_connection(url, 'passing', '//a[contains(@href,"#team-squad-archive-stats-passing")]')
        
    player_passing_df =  create_crawler_empty_df(list_of_extra_columns = who_scored_simple_columns['passing'], are_sub_games_existent = True)

    elements = driver.find_elements("css selector","#player-table-statistics-body tr") 
    #print(f"Number of Elements {len(elements)}")

    print('Fetching Player Table')

    # start process    
    now = time.time()

    for element in elements:
        if(len(element.find_elements("css selector","td")) < 14): continue 

        player_dict = create_dictionary_row_for_crawler(element, list_of_extra_columns = who_scored_simple_columns['passing'], are_sub_games_existent = True)

        player_passing_df.loc[len(player_passing_df)] = player_dict

    # end of the process
    later = time.time()
    # compute process time
    difference = float(later - now)

    print(f"[TIME LOG 3 PASSING] - Fetching Player Data took {difference} seconds")
    logging.info(f"[TIME LOG 3 PASSING] - Fetching Player Data took {difference} seconds")    
    
    print('Close Webdriver')
    driver.close()
    

    # Replace - with 0 among stats
    player_passing_df = replace_pd(player_passing_df)
    # Remove Nan value rows
    player_passing_df = remove_nan_values_added_while_scrapping(player_passing_df)
    
    # end of the whole process
    later_total = time.time()
    # compute the whole process time
    difference_total = float(later_total - now_total)

    print(f"[TIME LOG FINAL PASSING] - Whole Process took {difference_total} seconds")
    logging.info(f"[TIME LOG FINAL PASSING] - Whole Process took {difference_total} seconds") 

    print("[LOG PASSING] - Offensive Fetching Done")
    logging.info("[LOG PASSING] - Offensive Fetching Done") 

    return player_passing_df



driver_singleton = None
#keep connection alive and switch between categories to be read
def establish_driver_connection_for_detailed_section(url, xpath_for_current_or_archive, stats_selection = "Shots", is_circumstance_needed = True, circumstance_selection_text = 'Zones', stats_period_selection = 'Total', api_delay_term = API_DELAY_FOR_YOUR_PC):
    global driver_singleton
    # start of the process
    now = time.time()

    if driver_singleton == None: 
        driver_singleton = establish_driver_connection(url, 'detailed', xpath_for_current_or_archive)
    driver = driver_singleton

    select = Select(driver.find_element("id","category"))

    # Tackles, Interceptions, Fouls, Cards, Offsides, Clearances, Blocks, Saves
    # Shots, Goals, Dribbles, Possession Lost, Aerial
    # Passes, Key Passes, Assists
    print(f"Stats Option {stats_selection}")
    select.select_by_visible_text(stats_selection)
    time.sleep(api_delay_term)

    # Zones, Situations, Accuracy, Body Part, Lenght, Type
    if is_circumstance_needed:
        print(f"Circumstance Option {circumstance_selection_text}")
        select = Select(driver.find_element("id","subcategory"))
        select.select_by_visible_text(circumstance_selection_text)
        time.sleep(api_delay_term)


    select = Select(driver.find_element("id","statsAccumulationType"))

    print(f"Stats Period {stats_period_selection}")
    # Total, Per game, Per 90 minutes, Total
    select.select_by_visible_text(stats_period_selection)
    button = driver.find_element("class name", "search-button")

    driver.execute_script("arguments[0].click();", button);
    time.sleep(api_delay_term)

    # end of the process
    later = time.time()
    # compute process time
    difference = float(later - now)

    print(f"[TIME LOG 1.1] - Establishing Detailed Driver Connection took {difference} seconds")
    logging.info(f"[TIME LOG 1.1] - Establishing Detailed Driver Connection took {difference} seconds")



    return driver 


def crawl_player_team_stats_detailed(url, category = "offensive", is_current_season = False):
    global driver_singleton
    global fetching_data_counter, fetching_data_time_sum

    subcategory_mapping = whoscored_detailed_options[category]

    list_df = []
    index = 0 
    
    # start of the whole process
    now_total = time.time()
    
    for subcategory, conditions  in subcategory_mapping.items():
        print(subcategory)
        if(conditions[0]==[]):
            #print(conditions)
            columns = conditions[1]
            print(f'None -> {columns}')
            if is_current_season:
                driver = establish_driver_connection_for_detailed_section(url, '//a[contains(@href,"#team-squad-stats-detailed")]', subcategory, is_circumstance_needed = False, stats_period_selection = 'Total')
            else:
                driver = establish_driver_connection_for_detailed_section(url, '//a[contains(@href,"#team-squad-archive-stats-detailed")]', subcategory, is_circumstance_needed = False, stats_period_selection = 'Total')
            
            player_detailed_df =  create_crawler_empty_df(columns, are_sub_games_existent = False)

            # TRIAL TO BY BY PASS STALE STATE
            ignored_exceptions = (NoSuchElementException,StaleElementReferenceException,)
            elements = WebDriverWait(driver, 2.0, ignored_exceptions = ignored_exceptions)\
                .until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#player-table-statistics-body tr")))

            elements = driver.find_elements("css selector","#player-table-statistics-body tr") 
            
            # start process    
            now = time.time()
            
            print('Fetching Player Table')
            for element in elements:
                player_dict = create_dictionary_row_for_crawler(element, columns, False)

                player_detailed_df.loc[len(player_detailed_df)] = player_dict

            # end of the process
            later = time.time()
            # compute process time
            difference = float(later - now)

            print(f"[TIME LOG 3 DETAILED {category.upper()} | {subcategory.upper()}] - Fetching Player Data took {difference} seconds")
            logging.info(f"[TIME LOG 3 DETAILED {category.upper()} | {subcategory.upper()}] - Fetching Player Data took {difference} seconds")  

            fetching_data_counter += 1
            fetching_data_time_sum += difference

            # Replace - with 0 among stats
            player_detailed_df = replace_pd(player_detailed_df)
            # Remove Nan value rows
            player_detailed_df = remove_nan_values_added_while_scrapping(player_detailed_df)

            #player_detailed_df.to_csv(f"test_detail_scrapper/detailed_{category}_{index}.csv")
            #index += 1

            list_df.append(player_detailed_df)
        else:
            #print(conditions)
            characteristics = conditions[0]
            columns = conditions[1]
            index_columns = 0
            for characteristic in  characteristics:
                print(f'{characteristic} -> {columns[index_columns]}')
                if is_current_season:
                    driver = establish_driver_connection_for_detailed_section(url, '//a[contains(@href,"#team-squad-stats-detailed")]', subcategory, is_circumstance_needed = True, circumstance_selection_text = characteristic, stats_period_selection = 'Total')
                else:
                    driver = establish_driver_connection_for_detailed_section(url, '//a[contains(@href,"#team-squad-archive-stats-detailed")]', subcategory, is_circumstance_needed = True, circumstance_selection_text = characteristic, stats_period_selection = 'Total')
                
                player_detailed_df =  create_crawler_empty_df(columns[index_columns], are_sub_games_existent = False)
                
                # TRIAL TO BY BY PASS STALE STATE
                ignored_exceptions = (NoSuchElementException,StaleElementReferenceException,)
                elements = WebDriverWait(driver, 2.0, ignored_exceptions = ignored_exceptions)\
                    .until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#player-table-statistics-body tr")))

                elements = driver.find_elements("css selector","#player-table-statistics-body tr") 
                print('Fetching Player Table')
                
                # start process    
                now = time.time()
            
                for element in elements:
                    player_dict = create_dictionary_row_for_crawler(element, columns[index_columns], False)

                    player_detailed_df.loc[len(player_detailed_df)] = player_dict
                # end of the process
                later = time.time()
                # compute process time
                difference = float(later - now)

                print(f"[TIME LOG 3 DETAILED {category.upper()} | {subcategory.upper()} - {characteristic.upper()} ] - Fetching Player Data took {difference} seconds")
                logging.info(f"[TIME LOG 3 DETAILED {category.upper()} | {subcategory.upper()} - {characteristic.upper()}] - Fetching Player Data took {difference} seconds")  

                fetching_data_counter += 1
                fetching_data_time_sum += difference

                # Replace - with 0 among stats
                player_detailed_df = replace_pd(player_detailed_df)
                # Remove Nan value rows
                player_detailed_df = remove_nan_values_added_while_scrapping(player_detailed_df)
                
                #player_detailed_df.to_csv(f"test_detail_scrapper/detailed_{category}_{index}.csv")
                #index += 1

                list_df.append(player_detailed_df)    

                index_columns +=1

    #print("AJUNGE AICI 1")
    player_detailed_df = None
    for df in list_df:
        print(df.head(5))
        if player_detailed_df is None:
            player_detailed_df = df
        else:
            if 'total_shots' in df.columns:
                df = df.drop(['total_shots'], axis = 1)
            if 'total_goals' in df.columns:
                df = df.drop(['total_goals'], axis = 1)
            df = df.drop(['Unnamed: 0','name','age','position','tall','weight','games','mins','rating'],axis=1)

            player_detailed_df = pd.merge(player_detailed_df, df,on = ['player_number'])
            player_detailed_df  = player_detailed_df[player_detailed_df.columns.drop(list(player_detailed_df.filter(regex="Unnamed")))]
    #print('FINAL DF')
    #print(player_detailed_df)
    #print(player_detailed_df.columns)
    
    #driver.close()
    driver_singleton.close()
    driver_singleton = None

    # end of the whole process
    later_total = time.time()
    # compute the whole process time
    difference_total = float(later_total - now_total)

    print(f"[TIME LOG FINAL DETAILED {category.upper()}] - Whole Process took {difference_total} seconds")
    logging.info(f"[TIME LOG FINAL DETAILED {category.upper()}] - Whole Process took {difference_total} seconds") 

    print(f"[LOG DETAILED {category.upper()}] - {category.capitalize()} Fetching Done")
    logging.info(f"[LOG DETAILED {category.upper()}] - {category.capitalize()} Fetching Done") 

    return player_detailed_df


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

    # CREAZA FISIER  INTAI test_detail_scrapper 
    # verifica pentru defensive passing grija ca sunt Total nu Per game stats in cazul asta de baza
    #df = crawl_player_team_stats_summary("https://www.whoscored.com/Teams/65")
    #df = crawl_player_team_stats_summary("https://www.whoscored.com/Teams/65/Archive/?stageID=19895")
    #df = crawl_player_team_stats_passing("https://www.whoscored.com/Teams/65/Archive/?stageID=19895", False)
    
    #df = crawl_player_team_stats_detailed("https://www.whoscored.com/Teams/26/Archive/?stageID=5476","offensive", False)
    
    # once first is run incearca sa comentezi linia 770 si sa o decomentezi pe 773 
    # 775 824 834
    df = crawl_player_team_stats_detailed("https://www.whoscored.com/Teams/67/Archive/?stageId=3218","passing", False)

    df.to_csv("detail_scrapper_df.csv")
    #df.to_csv("scrapper_df.csv")

    # ONCE DONE

    # What to modify for each type of statistic
    # put instead of stat offensive, deffensive, passing and detailed_offensive, detailed_defensive, detailed_passing
    # George passing, detailed_offensive
    # Sergiu defensive, detailed_defensive, detailed_passing
    # modificati doar la stat si decomentati 786- 789


    # for league, teams_details in whoscored_teams_dict.items():
    #     print(league, '->', teams_details)
    #     crawl_chosen_stats_between_years(league, teams_details, 2020, 2023, stat = "detailed_passing")
    
    # for team, code in whoscored_teams_dict['la liga'].items():
    #     dict_of_league_urls = crawl_all_urls_for_given_team_in_league_competitions(code, "la liga", last_season_year = 2022 , first_season_year = 2001)
    #     print(f'{team} : {dict_of_league_urls}')
    #     break

