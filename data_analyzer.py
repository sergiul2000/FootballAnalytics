from distutils.command.build_scripts import first_line_re
from random import betavariate
import pandas as pd
from math import exp,pow

import py
pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None  

from math import gamma, exp


def compute_pythagorean_probability_for_given_goals(number_of_goals, alpha_goals_scored, alpha_goals_against, pythagorian_exponent, is_win):
    # for winning team:
    # exponetial( -(c+1/aGS)^y) exponetial( -(c/aGS)^y)
    # or 
    # for losing team:
    # 1- exponential( -(c+1/aGS)^y)
    
    if is_win:
        print(f'G {number_of_goals} alphaGS {alpha_goals_scored} alphaGA {alpha_goals_against} pythEXP {pythagorian_exponent}')
        first_element = exp(-pow(((number_of_goals+1)/alpha_goals_scored), pythagorian_exponent)) - exp(-pow(((number_of_goals)/alpha_goals_scored),pythagorian_exponent))
        
        second_element = 1 - exp(-pow((number_of_goals)/alpha_goals_against ,pythagorian_exponent))

        print(f'Win First {first_element} Second {second_element}')

        return first_element * second_element
    else:
        print(f'G {number_of_goals} alphaGS {alpha_goals_scored} alphaGA {alpha_goals_against} pythEXP {pythagorian_exponent}')
        first_element =  exp(-pow(((number_of_goals+1)/alpha_goals_scored),pythagorian_exponent)) - exp(-pow(((number_of_goals)/alpha_goals_scored),pythagorian_exponent))
        second_element = exp(-pow(((number_of_goals+1)/alpha_goals_against) ,pythagorian_exponent)) - exp(-pow(((number_of_goals)/alpha_goals_against) ,pythagorian_exponent))
        print(f'Draw First {first_element} Second {second_element}') 
        return first_element * second_element

def compute_points_per_game_pythagorian_estimation(limit_for_goals_iteration, alpha_goals_scored,alpha_goals_against, pythagorian_exponent):
    win_probability = sum(compute_pythagorean_probability_for_given_goals(goal, alpha_goals_scored, alpha_goals_against, pythagorian_exponent,True) for goal in range(0,limit_for_goals_iteration))
    draw_probability = sum(compute_pythagorean_probability_for_given_goals(goal, alpha_goals_scored, alpha_goals_against, pythagorian_exponent,False)  for goal in range(0,limit_for_goals_iteration))
    # 3 points for win
    # 1 point for draw
    print(f" WIN PROB {win_probability} ")
    print(f" DRAW PROB {win_probability} ")
    return (3 * win_probability) + draw_probability

def apply_pythagorian_league_table_stats(league, year):
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
    y = round(3*(mean-median)/standard_deviation,2)
    print(f"SKEWNESS {y}")

    K = gamma(1+(1/y))


    #alpha GS
    df_to_analyze['alphaGS'] = df_to_analyze['GoalsScored'].apply(lambda GS: round((GS-beta)/gamma(1+(1/y)),2))
    #alpha GR
    df_to_analyze['alphaGA'] = df_to_analyze['GoalsReceived'].apply(lambda GA: round((GA-beta)/gamma(1+(1/y)),2))

    df_to_analyze['AvgGS'] = df_to_analyze['GoalsScored']/df_to_analyze['Matches']
    df_to_analyze['AvgGA'] = df_to_analyze['GoalsReceived']/df_to_analyze['Matches']

    # df_to_analyze['AvgGS_Int'] = df_to_analyze['AvgGA'].astype('int')
    # df_to_analyze['AvgGA_Int'] = df_to_analyze['AvgGA'].astype('int')

    for index,row in df_to_analyze.iterrows():
        print(row)
        points = row['Matches']*compute_points_per_game_pythagorian_estimation(int(row['AvgGS']+1), row['alphaGS'], row['alphaGA'], y)
        print(f'POINTS {points}')
        break
        if index == 5:
            break



    # df_to_analyze['Win_Pythagorean'] = sum(exp(total_goal) for total_goal in range(0, df_to_analyze['AvgGS_Int']))
    # #df_to_analyze['Draw_Pythagorean'] =
    # print(df_to_analyze['Win_Pythagorean'])

    # df_to_analyze['Points_Pythagorean'] = (3 * df_to_analyze['Win_Probability'])+ df_to_analyze['Draw_Probability']
    
    
    # c variaza numarul de goluri 0, N



    #print(df_to_analyze)





if __name__ == '__main__':
    # print(sum(20*i for i in range(100, 200)))

    apply_pythagorian_league_table_stats('bundesliga', 2015)
    # for year in range(2014,2022):
    #     print(f'{year} - {year+1}')
    #     apply_pythagorian_league_table_stats('bundesliga',year)