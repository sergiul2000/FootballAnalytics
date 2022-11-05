from who_scored_crawler import crawl_all_urls_for_given_team_in_league_competitions, crawl_player_team_stats_detailed , save_stats_csv
from constants import whoscored_teams_dict
from os import walk
import pandas as pd



def merge(dict1, dict2, team_name):
    for i in dict2.keys():
        #print(i)
        team_name = team_name.replace(" ","_")
        index = f'{team_name}_{i}' 
        dict1[index] = dict2[i]
    return dict1

#league_dict = crawl_all_urls_for_given_team_in_league_competitions(65, 'la liga', first_season_year = 2009,last_season_year = 2023)
#print(league_dict)

statistic = 'detailed_passing'
paths = {}
league_dict = {}

league_dict = {
    'Real_Madrid_la liga_2022_2023': 'https://www.whoscored.com/Teams/52', 'Real_Madrid_la liga_2021_2022': 'https://www.whoscored.com/Teams/52/Archive/?stageId=19895', 'Real_Madrid_la liga_2020_2021': 'https://www.whoscored.com/Teams/52/Archive/?stageId=18851', 'Real_Madrid_la liga_2019_2020': 'https://www.whoscored.com/Teams/52/Archive/?stageId=17702', 'Real_Madrid_la liga_2018_2019': 'https://www.whoscored.com/Teams/52/Archive/?stageId=16546', 'Real_Madrid_la liga_2017_2018': 'https://www.whoscored.com/Teams/52/Archive/?stageId=15375', 'Real_Madrid_la liga_2016_2017': 'https://www.whoscored.com/Teams/52/Archive/?stageId=13955', 'Real_Madrid_la liga_2015_2016': 'https://www.whoscored.com/Teams/52/Archive/?stageId=12647', 'Real_Madrid_la liga_2014_2015': 'https://www.whoscored.com/Teams/52/Archive/?stageId=11363', 'Real_Madrid_la liga_2013_2014': 'https://www.whoscored.com/Teams/52/Archive/?stageId=7920', 'Real_Madrid_la liga_2012_2013': 'https://www.whoscored.com/Teams/52/Archive/?stageId=6652', 'Real_Madrid_la liga_2011_2012': 'https://www.whoscored.com/Teams/52/Archive/?stageId=5577', 'Real_Madrid_la liga_2010_2011': 'https://www.whoscored.com/Teams/52/Archive/?stageId=4624', 'Real_Madrid_la liga_2009_2010': 'https://www.whoscored.com/Teams/52/Archive/?stageId=3218', 
    'Barcelona_la liga_2022_2023': 'https://www.whoscored.com/Teams/65', 'Barcelona_la liga_2021_2022': 'https://www.whoscored.com/Teams/65/Archive/?stageId=19895', 'Barcelona_la liga_2020_2021': 'https://www.whoscored.com/Teams/65/Archive/?stageId=18851', 'Barcelona_la liga_2019_2020': 'https://www.whoscored.com/Teams/65/Archive/?stageId=17702', 'Barcelona_la liga_2018_2019': 'https://www.whoscored.com/Teams/65/Archive/?stageId=16546', 'Barcelona_la liga_2017_2018': 'https://www.whoscored.com/Teams/65/Archive/?stageId=15375', 'Barcelona_la liga_2016_2017': 'https://www.whoscored.com/Teams/65/Archive/?stageId=13955', 'Barcelona_la liga_2015_2016': 'https://www.whoscored.com/Teams/65/Archive/?stageId=12647', 'Barcelona_la liga_2014_2015': 'https://www.whoscored.com/Teams/65/Archive/?stageId=11363', 'Barcelona_la liga_2013_2014': 'https://www.whoscored.com/Teams/65/Archive/?stageId=7920', 'Barcelona_la liga_2012_2013': 'https://www.whoscored.com/Teams/65/Archive/?stageId=6652', 'Barcelona_la liga_2011_2012': 'https://www.whoscored.com/Teams/65/Archive/?stageId=5577', 'Barcelona_la liga_2010_2011': 'https://www.whoscored.com/Teams/65/Archive/?stageId=4624', 'Barcelona_la liga_2009_2010': 'https://www.whoscored.com/Teams/65/Archive/?stageId=3218', 
    'Atletico_Madrid_la liga_2022_2023': 'https://www.whoscored.com/Teams/63', 'Atletico_Madrid_la liga_2021_2022': 'https://www.whoscored.com/Teams/63/Archive/?stageId=19895', 'Atletico_Madrid_la liga_2020_2021': 'https://www.whoscored.com/Teams/63/Archive/?stageId=18851', 'Atletico_Madrid_la liga_2019_2020': 'https://www.whoscored.com/Teams/63/Archive/?stageId=17702', 'Atletico_Madrid_la liga_2018_2019': 'https://www.whoscored.com/Teams/63/Archive/?stageId=16546', 'Atletico_Madrid_la liga_2017_2018': 'https://www.whoscored.com/Teams/63/Archive/?stageId=15375', 'Atletico_Madrid_la liga_2016_2017': 'https://www.whoscored.com/Teams/63/Archive/?stageId=13955', 'Atletico_Madrid_la liga_2015_2016': 'https://www.whoscored.com/Teams/63/Archive/?stageId=12647', 'Atletico_Madrid_la liga_2014_2015': 'https://www.whoscored.com/Teams/63/Archive/?stageId=11363', 'Atletico_Madrid_la liga_2013_2014': 'https://www.whoscored.com/Teams/63/Archive/?stageId=7920', 'Atletico_Madrid_la liga_2012_2013': 'https://www.whoscored.com/Teams/63/Archive/?stageId=6652', 'Atletico_Madrid_la liga_2011_2012': 'https://www.whoscored.com/Teams/63/Archive/?stageId=5577', 'Atletico_Madrid_la liga_2010_2011': 'https://www.whoscored.com/Teams/63/Archive/?stageId=4624', 'Atletico_Madrid_la liga_2009_2010': 'https://www.whoscored.com/Teams/63/Archive/?stageId=3218', 
    'Sevilla_la liga_2022_2023': 'https://www.whoscored.com/Teams/67', 'Sevilla_la liga_2021_2022': 'https://www.whoscored.com/Teams/67/Archive/?stageId=19895', 'Sevilla_la liga_2020_2021': 'https://www.whoscored.com/Teams/67/Archive/?stageId=18851', 'Sevilla_la liga_2019_2020': 'https://www.whoscored.com/Teams/67/Archive/?stageId=17702', 'Sevilla_la liga_2018_2019': 'https://www.whoscored.com/Teams/67/Archive/?stageId=16546', 'Sevilla_la liga_2017_2018': 'https://www.whoscored.com/Teams/67/Archive/?stageId=15375', 'Sevilla_la liga_2016_2017': 'https://www.whoscored.com/Teams/67/Archive/?stageId=13955', 'Sevilla_la liga_2015_2016': 'https://www.whoscored.com/Teams/67/Archive/?stageId=12647', 'Sevilla_la liga_2014_2015': 'https://www.whoscored.com/Teams/67/Archive/?stageId=11363', 'Sevilla_la liga_2013_2014': 'https://www.whoscored.com/Teams/67/Archive/?stageId=7920', 'Sevilla_la liga_2012_2013': 'https://www.whoscored.com/Teams/67/Archive/?stageId=6652', 'Sevilla_la liga_2011_2012': 'https://www.whoscored.com/Teams/67/Archive/?stageId=5577', 'Sevilla_la liga_2010_2011': 'https://www.whoscored.com/Teams/67/Archive/?stageId=4624', 'Sevilla_la liga_2009_2010': 'https://www.whoscored.com/Teams/67/Archive/?stageId=3218', 
    'Valencia_la liga_2022_2023': 'https://www.whoscored.com/Teams/55', 'Valencia_la liga_2021_2022': 'https://www.whoscored.com/Teams/55/Archive/?stageId=19895', 'Valencia_la liga_2020_2021': 'https://www.whoscored.com/Teams/55/Archive/?stageId=18851', 'Valencia_la liga_2019_2020': 'https://www.whoscored.com/Teams/55/Archive/?stageId=17702', 'Valencia_la liga_2018_2019': 'https://www.whoscored.com/Teams/55/Archive/?stageId=16546', 'Valencia_la liga_2017_2018': 'https://www.whoscored.com/Teams/55/Archive/?stageId=15375', 'Valencia_la liga_2016_2017': 'https://www.whoscored.com/Teams/55/Archive/?stageId=13955', 'Valencia_la liga_2015_2016': 'https://www.whoscored.com/Teams/55/Archive/?stageId=12647', 'Valencia_la liga_2014_2015': 'https://www.whoscored.com/Teams/55/Archive/?stageId=11363', 'Valencia_la liga_2013_2014': 'https://www.whoscored.com/Teams/55/Archive/?stageId=7920', 'Valencia_la liga_2012_2013': 'https://www.whoscored.com/Teams/55/Archive/?stageId=6652', 'Valencia_la liga_2011_2012': 'https://www.whoscored.com/Teams/55/Archive/?stageId=5577', 'Valencia_la liga_2010_2011': 'https://www.whoscored.com/Teams/55/Archive/?stageId=4624', 'Valencia_la liga_2009_2010': 'https://www.whoscored.com/Teams/55/Archive/?stageId=3218', 
    'Villarreal_la liga_2022_2023': 'https://www.whoscored.com/Teams/839', 'Villarreal_la liga_2021_2022': 'https://www.whoscored.com/Teams/839/Archive/?stageId=19895', 'Villarreal_la liga_2020_2021': 'https://www.whoscored.com/Teams/839/Archive/?stageId=18851', 'Villarreal_la liga_2019_2020': 'https://www.whoscored.com/Teams/839/Archive/?stageId=17702', 'Villarreal_la liga_2018_2019': 'https://www.whoscored.com/Teams/839/Archive/?stageId=16546', 'Villarreal_la liga_2017_2018': 'https://www.whoscored.com/Teams/839/Archive/?stageId=15375', 'Villarreal_la liga_2016_2017': 'https://www.whoscored.com/Teams/839/Archive/?stageId=13955', 'Villarreal_la liga_2015_2016': 'https://www.whoscored.com/Teams/839/Archive/?stageId=12647', 'Villarreal_la liga_2014_2015': 'https://www.whoscored.com/Teams/839/Archive/?stageId=11363', 'Villarreal_la liga_2013_2014': 'https://www.whoscored.com/Teams/839/Archive/?stageId=7920', 'Villarreal_la liga_2011_2012': 'https://www.whoscored.com/Teams/839/Archive/?stageId=5577', 'Villarreal_la liga_2010_2011': 'https://www.whoscored.com/Teams/839/Archive/?stageId=4624', 'Villarreal_la liga_2009_2010': 'https://www.whoscored.com/Teams/839/Archive/?stageId=3218'
    }

#print(league_dict)
for league, team_details in whoscored_teams_dict.items():

    print(f'LEAGUE {league}')
    # for team_name, team_id in team_details.items():
    #     print(f'{team_name} {team_id}')

    #     team_dict = crawl_all_urls_for_given_team_in_league_competitions(team_id, 'la liga', first_season_year = 2009,last_season_year = 2023)
    #     league_dict = merge(league_dict, team_dict, team_name)
    #     print(league_dict)
        
    # print(f'LEAGUE DICT {league_dict}')
    
    # break
    
    count = 0
    for year in range(2009,2023):

        #print(f'Year {year}')
        path = f'dataframes/whoscored_player_{statistic}_stats_1/{league}/season_{year}_{year+1}'
        #print(path)
        filenames = next(walk(path), (None, None, []))[2]
        filenames = [f'{path}/{filename}' for filename in filenames]


        for file_name in filenames:
            csv = pd.read_csv(file_name)

            # CSV is empty
            if len(csv.index) == 0:
                count += 1
                print(f"# {count}")
                #print(f"{file_name}")    

                part = file_name.split('/')[4]
                team_name = part.split('_passing')[0]
                season_part = part.split('season_')[1].replace('.csv','')
                
                league_dict_key = f'{team_name}_la liga_{season_part}'
                url = league_dict[league_dict_key]

                print(f'{file_name} {url}')
                
                is_current_season = True

                if 'Archive' in url:
                    is_current_season = False

                # Crawl again
                df_detailed_passing = crawl_player_team_stats_detailed(url, "passing", is_current_season)
                
                save_stats_csv(df_detailed_passing,'detailed_passing',league, team_name, season_start_year = year)                





    break 




# text = 'dataframes/whoscored_player_detailed_passing_stats_1/la liga/season_2021_2022/Atletico_Madrid_passing_stats_in_season_2021_2022.csv'
# part = text.split('/')[4]
# team_name = part.split('_passing')[0]
# #print(team_name)
# season_part = part.split('season_')[1].replace('.csv','')
# #print(season_part)
# league_dict_key = f'{team_name}_la liga_{season_part}'
# print(league_dict_key)