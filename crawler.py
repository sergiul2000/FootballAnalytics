import time
import numpy as np
import pandas as pd
import time
import pickle
import sys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support.select import Select

def replace_pd(df):
    mapping = {'-': 0} 
    
    replace_dict = {}
    
    for colum in df.columns:
        replace_dict[colum] = mapping
    return df.replace(replace_dict)

def crawl_players_team_stats_for_available_seasons_by_competition(team_id, competition_name):
    dict_of_league_urls = crawl_all_urls_for_given_team_in_league_competitions(team_id, competition_name)


    for item in dict_of_league_urls.items():
        print(item)
        df_season_stats = crawl_player_team_stats_summary(item[1])
        df_season_stats.to_csv(f'test/Barcelona_season_{item[0]}')



def crawl_all_urls_for_given_team_in_league_competitions(team_id, competition_name):
    url_current_season = f'https://www.whoscored.com/Teams/{team_id}'
    url = f'https://www.whoscored.com/Teams/{team_id}/Archive'
    dict_of_league_competitions_urls = dict()
    dict_of_league_competitions_urls['2022_2023'] = url_current_season

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    print('Installing Chrome driver')
    driver.get(url)

    dropDown = driver.find_element("id","stageId")
    select = Select(dropDown)
    for option in select.options:
        #print(option.get_attribute('value'))
        #print(option.text)
        value = option.get_attribute('value')

        
        if competition_name in option.text:
            season_full = option.text.split('-')[1][1:]
            start_year = season_full.split('/')[0]
            end_season = season_full.split('/')[1]
            season_text = f'{start_year}_{end_season}'
            print(season_text)

            url_to_append = f'https://www.whoscored.com/Teams/{team_id}/Archive/?stageId={value}'
            dict_of_league_competitions_urls[season_text] = url_to_append

    print(dict_of_league_competitions_urls)
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
    print('Waiting for getting data')
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

        print(f'Populating CSV with {player_dict}')
        player_summary_df.loc[len(player_summary_df)] = player_dict
       
    
    # close webdriver
    print('Close Webdriver')
    driver.close()

    player_summary_df['position'] = player_summary_df['position'].str.replace('"','')

    for i,row in player_summary_df.iterrows():
        print(row['games'])
        parts = row['games'].split("(")
        print(parts)
        if(len(parts)==2):
            player_summary_df.at[i,'start_games'] = parts[0]
            print(parts[1])
            player_summary_df.at[i,'sub_games'] = parts[1].replace(')','')
        else:
            player_summary_df.at[i,'start_games'] = row['games']
            player_summary_df.at[i,'sub_games'] =  0
    #print(row) 
    
    return player_summary_df

if __name__ == "__main__":
    #65 barcelona | 26 liverpool
    # Barcelona = crawl_player_team_stats_summary(65, api_delay_term=5)
    # Barcelona = replace_pd(Barcelona)
    # print(Barcelona)
    # Barcelona.to_csv("Barcelona.csv")

    #crawl_all_urls_for_given_team_in_league_competitions(65, "LaLiga")
    crawl_players_team_stats_for_available_seasons_by_competition(65, "LaLiga")