from re import X
from constants import whoscored_teams_dict

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

        for item in dict_of_league_urls.items():
            print(item)
            
            match stat:
                case 'summary':
                    df_season_stats = crawl_player_team_stats_summary(item[1])
                    
                    save_stats_csv(df_season_stats,'summary',league, team, season_start_year = int(item[0].split('_')[1]))
                case 'offensive':
                    #To Be Implemented
                    print('2')
                case 'defensive':
                    #To Be Implemented
                    print('3')
                case 'detailed':
                    #To Be Implemented
                    print('4')
                case _:
                    #To Be Implemented
                    print('nada')      


def crawl_players_team_stats_for_available_seasons_by_competition(team_id, competition_name):

    dict_of_league_urls = crawl_all_urls_for_given_team_in_league_competitions(team_id, competition_name)

    for item in dict_of_league_urls.items():
        print(item)
        df_season_stats = crawl_player_team_stats_summary(item[1])
    
        df_season_stats.to_csv(f'test/Barcelona_season_{item[0]}.csv')


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


def crawl_player_team_stats_summary(url, api_delay_term=5):
    """
    crawling player statistics of certain team
    
    Args :
        team_id : team number 
        
    return :
        player statistics (dataframe)
    
    """

    # connect webdriver
    #url = "https://www.whoscored.com/Teams/" + str(team_id)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    print('Installing Chrome driver')
    driver.get(url)

    # wait for getting data
    print('Waiting to get data')
    time.sleep(api_delay_term)
    
    # make pandas dataframe
    player_summary_df = pd.DataFrame(columns=[
        "player_number", "name", "age", "position", "tall", "weight", "games",
        "mins", "goals", "assists", "yel", "red", "spg", "ps", "aw", "motm", "rating"
        ])
    
    # get player summay datas
    #elements = driver.find_elements_by_css_selector("#player-table-statistics-body tr")
    elements = driver.find_elements("css selector","#player-table-statistics-body tr") 

    print('Fetching Player Table')

    for element in elements:

        player_dict = { 
            "player_number": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].get_attribute("href").split("/")[4],
            "name": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].find_elements("css selector","span")[0].text,
            "age": element.find_elements("class name","player-meta-data")[0].text,
            "position": element.find_elements("class name","player-meta-data")[1].text[1:],
            "tall": element.find_elements("css selector","td")[2].text,
            "weight": element.find_elements("css selector","td")[3].text,
            "games": element.find_elements("css selector","td")[4].text,
            "mins": element.find_elements("css selector","td")[5].text,
            "goals": element.find_elements("css selector","td")[6].text,
            "assists": element.find_elements("css selector","td")[7].text,
            "yel": element.find_elements("css selector","td")[8].text,
            "red": element.find_elements("css selector","td")[9].text,
            "spg": element.find_elements("css selector","td")[10].text,
            "ps": element.find_elements("css selector","td")[11].text,
            "aw": element.find_elements("css selector","td")[12].text,
            "motm": element.find_elements("css selector","td")[13].text, 
            "rating": element.find_elements("css selector","td")[14].text,  
        }

        #print(f'Populating CSV with {player_dict}')
        player_summary_df.loc[len(player_summary_df)] = player_dict
       
    
    # close webdriver
    print('Close Webdriver')
    driver.close()

    player_summary_df['position'] = player_summary_df['position'].str.replace('"','')

    for i,row in player_summary_df.iterrows():
        #print(row['games'])
        parts = row['games'].split("(")
        #print(parts)
        if(len(parts)==2):
            player_summary_df.at[i,'start_games'] = parts[0]
            #print(parts[1])
            player_summary_df.at[i,'sub_games'] = parts[1].replace(')','')
        else:
            player_summary_df.at[i,'start_games'] = row['games']
            player_summary_df.at[i,'sub_games'] =  0
    #print(row) 
    
    # Replace - with 0 among stats
    player_summary_df = replace_pd(player_summary_df)
    
    return player_summary_df

def crawl_player_team_stats_offensive(url, api_delay_term=5):
    return 0

def crawl_player_team_stats_defensive(url, api_delay_term=5):
    return 0

def crawl_player_team_stats_passing(url, api_delay_term=5):
    return 0

def crawl_player_team_stats_detailed(url, api_delay_term=5):
    return 0


if __name__ == "__main__":

    for league, teams_details in whoscored_teams_dict.items():
        print(league, '->', teams_details)
        crawl_chosen_stats_between_years(league, teams_details, 2009, 2023)


    # Correction already modified in code
    # for league, team_details in whoscored_teams_dict.items():
    #     # paths = []
    #     print(f'LEAGUE {league}')
    #     for year in range(2009,2023):
    #         print(f'Year {year}')
    #         path =f'dataframes/whoscored_player_summary_stats/{league}/season_{year}_{year+1}'
    #         filenames = next(walk(path), (None, None, []))[2]
    #         filenames = [f'{path}/{filename}' for filename in filenames]

    #         print(filenames)
    #         for file in filenames:
    #             print(f'File {file}')
    #             csv = pd.read_csv(file)
    #             csv = replace_pd(csv)
    #             csv.to_csv(file)
    #             print(csv.head(5))
                
    

