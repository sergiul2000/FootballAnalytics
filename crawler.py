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

#  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver.implicitly_wait(3)
# driver.get('https:/1xbet.whoscored.com/')
# driver.close()

def replace_pd(df):
    mapping = {'-': 0} 
    
    replace_dict = {}
    
    for colum in df.columns:
        replace_dict[colum] = mapping
    return df.replace(replace_dict)

# def replace_Apps(df):
    
#     sub = list()
#     for i in list(df['Apps']):
#         if '(' in i :
#             sub.append(i.split('(')[1].split(')')[0])
#         else :
#             sub.append('0')
#     df['sub'] = sub
#     df['Apps'] = list(map(lambda x: x.split('(')[0], list(df['Apps'])))
#     df['team_name'] = list(map(lambda x: x.split(',')[0], list(df['team_name'])))
#     return(df)        

def crawling_player_summary(team_id, api_delay_term=5):
    """
    crawling player statistics of certain team
    
    Args :
        team_id : team number 
        
    return :
        player statistics (dataframe)
    
    """

    # connect webdriver
    url = "https://www.whoscored.com/Teams/" + str(team_id)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    # wait for getting data
    time.sleep(api_delay_term)
    
    # make pandas dataframe
    player_summary_df = pd.DataFrame(columns=[
        "player_number", "name","age","position","tall","weight","games",
        "mins", "goals", "asists", "yel", "red", "spg", "ps","aw","motm", "rating"
        ])
    
    # get player summay datas
    #elements = driver.find_elements_by_css_selector("#player-table-statistics-body tr")
    elements = driver.find_elements("css selector","#player-table-statistics-body tr") 
    for element in elements:

        player_dict = { 
        #    "player_number": element.find_elements_by_css_selector("td")[0].find_elements_by_css_selector("a")[0].get_attribute("href").split("/")[1], 
        #     "name": element.find_elements_by_css_selector("td")[0].find_elements_by_css_selector("a")[0].find_elements_by_css_selector("span")[0].text,     
        #     "age": element.find_elements_by_css_selector("td")[1].find_elements_by_css_selector("span")[0].text,
        #     "position": element.find_elements_by_css_selector("td")[1].find_elements_by_css_selector("span")[1].text[1:], 

            "player_number": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].get_attribute("href").split("/")[4],
            "name": element.find_elements("css selector","td")[0].find_elements("css selector","a")[0].find_elements("css selector","span")[0].text,
            "age": element.find_elements("class name","player-meta-data")[0].text,
            "position": element.find_elements("class name","player-meta-data")[1].text[1:],
            "tall": element.find_elements("css selector","td")[2].text,
            "weight": element.find_elements("css selector","td")[3].text,
            "games": element.find_elements("css selector","td")[4].text,
            "mins": element.find_elements("css selector","td")[5].text,
            "goals": element.find_elements("css selector","td")[6].text,
            "asists": element.find_elements("css selector","td")[7].text,
            "yel": element.find_elements("css selector","td")[8].text,
            "red": element.find_elements("css selector","td")[9].text,
            "spg": element.find_elements("css selector","td")[10].text,
            "ps": element.find_elements("css selector","td")[11].text,
            "aw": element.find_elements("css selector","td")[12].text,
            "motm": element.find_elements("css selector","td")[13].text, 
            "rating": element.find_elements("css selector","td")[14].text  

        }
        
        player_summary_df.loc[len(player_summary_df)] = player_dict
    
    # close webdriver
    driver.close()
    
    return player_summary_df
Barcelona = crawling_player_summary(65, api_delay_term=5)
Barcelona = replace_pd(Barcelona)
print(Barcelona)
Barcelona.to_csv("Barcelona.csv")