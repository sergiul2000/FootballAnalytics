import pandas as pd
pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None  

import formulas
from math import gamma
from empty_folder_creator import create_empty_directories


# difference_pythagorian_simple_extended = 0

# mean_simple_sum = 0
# mean_extended_sum = 0

# number_of_seasons = 0


def analyze_differences_for_pythagorian_methods(serie_simple, serie_extended):
    print("CEVE")
    mean_simple = serie_simple.abs().mean()
    mean_extended = serie_extended.abs().mean()
    print(f'Delta Points Simple: {mean_simple}')
    print(f'Delta Points Extended: {mean_extended}')
    #print(f'Difference Between Simple and Extended: {mean_simple - mean_extended}')
    #difference_pythagorian_simple_extended = (mean_simple - mean_extended)
    #return abs(difference_pythagorian_simple_extended), mean_simple, mean_extended
    return mean_simple, mean_extended




def read_league_table_csv(league, year):
    path = f'dataframes/league_table/{league}/{league}_league_table_in_season_{year}_{year+1}.csv'

    df = pd.read_csv(path)
    #print(df.head(5))
    df_to_analyze = df[['Team','M','W','D', 'L', 'G', 'GA','PTS']]

    df_to_analyze.rename(columns = {'M':'Matches', 
                                    'W':'Wins', 
                                    'D':'Draws',
                                    'L':'Loses',
                                    'G':'GoalsScored',
                                    'GA':'GoalsReceived',
                                    'PTS':'Points',
                                    }, inplace=True)  

    #print(df_to_analyze.head(5))
    return df_to_analyze


def apply_pythagorian_league_table_stats(league, year):
    df_to_analyze = read_league_table_csv(league, year)

    # Simple Pythagorian Table creation

    y_best = 0
    rmse_min = 320000

    y = 1.0
    while y <= 2.0:
        y = round(y,2)
        # print(f'Trying for y {y}')
        # print(f'________________________________________________________________')

        df_simple_pythagorian, pythagorian_expectation_curent_y = formulas.compute_pythagorian_expectation(df_to_analyze, y)
        rmse_value = formulas.calculate_rmse(formulas.merge_lists(pythagorian_expectation_curent_y, df_simple_pythagorian['Points']), df_simple_pythagorian.size )

        if(rmse_value < rmse_min):
            rmse_min = rmse_value
            y_best = y

        y += 0.1

    rmse_min = format(rmse_min, ".2f")
    
    print('Rmse_min = ', rmse_min, ' y_best = ', y_best)

    best_y_column = f'Expected Points y = {y_best}'
    df_simple_pythagorian = df_simple_pythagorian[['Team','Matches','Wins','Draws','Loses','GoalsScored','GoalsReceived', 'Points', best_y_column]]
    df_simple_pythagorian.rename(columns={best_y_column:'Estimated_Points_Simple'}, inplace=True)
    df_simple_pythagorian['Delta_Points_Simple'] = df_simple_pythagorian['Points'] - df_simple_pythagorian['Estimated_Points_Simple']
    print(df_simple_pythagorian)

    
    # Extended Pythagorian Table creation

    beta = -0.5 # distribution parameter

    '''
    Skewness of pythagoric exponent
    Using Pearson's formula
    3 * (Mean – Median) / Standard Deviation
    VEZI ALTE FORMULE PENTRU SKEWNESS
    '''
    mean = df_to_analyze['GoalsScored'].mean()
    median = df_to_analyze['GoalsScored'].median()
    standard_deviation = df_to_analyze['GoalsScored'].std()
    y = round(3 * (mean-median) / standard_deviation, 2)
    # print(f"SKEWNESS {y}")
    
    K = gamma(1 + (1 / y))
    # print(f"K {K}")

    df_extended_pythagorian = read_league_table_csv(league, year)


    df_extended_pythagorian['AvgGS'] = df_extended_pythagorian['GoalsScored'] / df_extended_pythagorian['Matches']
    df_extended_pythagorian['AvgGA'] = df_extended_pythagorian['GoalsReceived'] / df_extended_pythagorian['Matches']

    #alpha GS
    df_extended_pythagorian['alphaGS'] = df_extended_pythagorian['GoalsScored'].apply(lambda GS: round((GS-beta)/K),2)
    #alpha GR
    df_extended_pythagorian['alphaGA'] = df_extended_pythagorian['GoalsReceived'].apply(lambda GA: round((GA-beta)/K),2)

    # alpha GS * K
    df_extended_pythagorian['alphaGGS'] = df_extended_pythagorian['alphaGS'].apply(lambda alphaGS: round(alphaGS * K,2) )
    #alpha GR * K
    df_extended_pythagorian['alphaGGA'] = df_extended_pythagorian['alphaGA'].apply(lambda alphaGA: round(alphaGA * K,2) )

    for index,row in df_extended_pythagorian.iterrows():
        #print(row)
        
        points_per_game_expectancy, win_expectancy, draw_expectancy = formulas.compute_points_per_game_pythagorian_estimation(1000, row['alphaGS'],row['alphaGGS'], row['alphaGA'], row['alphaGGA'],K ,y)
        points = int(row['Matches'] * points_per_game_expectancy)
        win_expectancy = int(row['Matches'] * win_expectancy)
        draw_expectancy = int(row['Matches'] * draw_expectancy) +1
        lose_expectancy = row['Matches'] - int(win_expectancy) - (int(draw_expectancy))

        df_extended_pythagorian.at[index,'Estimated_Wins_Extended'] = win_expectancy
        df_extended_pythagorian.at[index,'Estimated_Draws_Extended'] = draw_expectancy
        df_extended_pythagorian.at[index,'Estimated_Loses_Extended'] = lose_expectancy
        df_extended_pythagorian.at[index,'Estimated_Points_Extended'] =  points


    df_extended_pythagorian['Delta_Points_Extended'] = df_extended_pythagorian['Points'] - df_extended_pythagorian['Estimated_Points_Extended']

    df_extended_pythagorian['Delta_Merge'] = df_extended_pythagorian['Points'] - df_extended_pythagorian['Estimated_Points_Extended']

    print(df_extended_pythagorian)
    df_result = df_simple_pythagorian.merge(df_extended_pythagorian, how='right')


    df_result = df_result[['Team','Matches','Wins','Draws','Loses','GoalsScored','GoalsReceived', 'AvgGS', 'AvgGA', 'Estimated_Wins_Extended','Estimated_Draws_Extended','Estimated_Loses_Extended', 'Points','Estimated_Points_Simple', 'Delta_Points_Simple','Estimated_Points_Extended','Delta_Points_Extended']]
    
    #difference_pythagorian_simple_extended, mean_simple, mean_extended = analyze_differences_for_pythagorian_methods(df_result['Delta_Points_Simple'],df_result['Delta_Points_Extended'])
    mean_simple, mean_extended = analyze_differences_for_pythagorian_methods(df_result['Delta_Points_Simple'],df_result['Delta_Points_Extended'])
    
    # mean_simple = df_result['Delta_Points_Simple'].abs().mean()
    # mean_extended = df_result['Delta_Points_Extended'].abs().mean()
    # print(f'Delta Points Simple: {mean_simple}')
    # print(f'Delta Points Extended: {mean_extended}')
    
    print(df_result)

    create_empty_directories('dataframes', 'pythagorian_league_table', league, year, year+1, need_year=False)
    save_path = f'dataframes/pythagorian_league_table/{league}/{league}_pythagorian_league_table_in_season_{year}_{year+1}.csv'

    df_result.to_csv(save_path)

    #return difference_pythagorian_simple_extended, mean_simple, mean_extended
    return mean_simple, mean_extended





if __name__ == '__main__':
    # print(sum(20*i for i in range(100, 200)))
    

    #apply_pythagorian_league_table_stats('la liga', 2015)]
    difference_pythagorian_simple_extended_avg = 0

    mean_simple_sum = 0
    mean_extended_sum = 0

    number_of_seasons = 0
    for year in range(2014,2022):
        print(f'{year} - {year+1}')
        #difference_pythagorian_simple_extended, mean_simple, mean_extended = apply_pythagorian_league_table_stats('la liga',year)
            
        #difference_pythagorian_simple_extended_avg += difference_pythagorian_simple_extended
        mean_simple, mean_extended = apply_pythagorian_league_table_stats('la liga',year)
        

        mean_simple_sum += mean_simple
        mean_extended_sum += mean_extended

        number_of_seasons += 1

    print(f'Avg Delta Points Simple: {mean_simple_sum / number_of_seasons}')
    print(f'Avg Delta Points Extended: {mean_extended_sum / number_of_seasons}')
    print(f'Avg Difference Between Simple and Extended: {(mean_extended_sum - mean_simple_sum)/ number_of_seasons}')
