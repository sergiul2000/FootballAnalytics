import pandas as pd
pd.set_option('display.max_columns', None)



def apply_pythagorian_league_table_stats(league, year):
    path = f'dataframes/league_table/{league}/{league}_league_table_in_season_{year}_{year+1}.csv'

    df = pd.read_csv(path)
    #print(df.head(5))
    df_to_analyze = df[['Team','M','W','D', 'L', 'G', 'GA','PTS']]

    df_to_analyze.rename(columns = {'M':'GamesPlayed', 
                                    'W':'Wins', 
                                    'D':'Draws',
                                    'L':'Loses',
                                    'G':'GoalsScored',
                                    'GA':'GoalsAgainst',
                                    'PTS':'Points',
                                    }, inplace=True)  

    print(df_to_analyze['GoalsScored'])

    


if __name__ == '__main__':
    apply_pythagorian_league_table_stats('bundesliga',2021)