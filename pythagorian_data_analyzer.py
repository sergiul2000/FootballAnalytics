import math
from platform import win32_edition
from sklearn.linear_model import LinearRegression
from math import gamma, exp
import pandas as pd
from math import exp, pow
import statistics

pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None


#def pythagorean_expectation(goals_scored, goals_conceded, average_points_per_game, pythagorean_expectation):

    #pythagorean_expectation var is the PE from the article
    #pythagorean_expectation = pow(goals_scored, ga)

def frange(start, step, num):
    for i in range(num):
        yield start
        start += step

def compute_pythagorean_expectation(df, y):

    rmse = 0
    return rmse ,df


def generate_formula_for_all_teams(league,year):
    path = f'dataframes/league_table/{league}/{league}_league_table_in_season_{year}_{year + 1}.csv'

    df = pd.read_csv(path)
    df_to_analyze = df[['Team', 'M', 'W', 'D', 'L', 'G', 'GA', 'PTS']]

    df_to_analyze.rename(columns={'M': 'Matches',
                                  'W': 'Wins',
                                  'D': 'Draws',
                                  'L': 'Loses',
                                  'G': 'GoalsScored',
                                  'GA': 'GoalsReceived',
                                  'PTS': 'Points',
                                  }, inplace=True)


    df_to_analyze = df[['Team', 'M', 'W', 'D', 'L', 'G', 'GA', 'PTS']]

    #redenumim coloanele pentru a avea nume mai sugestive
    df_to_analyze.rename(columns={'M': 'Matches',
                                  'W': 'Wins',
                                  'D': 'Draws',
                                  'L': 'Loses',
                                  'G': 'GoalsScored',
                                  'GA': 'GoalsReceived',
                                  'PTS': 'Points',
                                  }, inplace=True)

    df_to_analyze['AvgGS'] = df_to_analyze['GoalsScored'] / df_to_analyze['Matches']
    df_to_analyze['AvgGA'] = df_to_analyze['GoalsReceived'] / df_to_analyze['Matches']



    y_best = 0
    rmse_min = 320000

    y = 1.0
    while y<=2.0:
        y = round(y,2)
        print(f'Trying for y {y}')
        print(f'________________________________________________________________')

        rmse_value,df_to_analyze = compute_pythagorian_expectation(df, y)


        if(rmse_value<rmse_min):
            rmse_min = rmse_value
            y_best = y

        y+=0.1

    rmse_value,df_to_analyze = compute_pythagorian_expectation(df, y_best)




    #gamma_coeficient = 1.2

    #print(df_to_analyze['Points'])
    ratio_win_lose = []
    ratio_draw = []
    average_points_per_game = []
    pythagorean_expectation = []

    for i in range(len(df_to_analyze)):
        curent_row = df_to_analyze.iloc[i]
        ratio_win_lose.append( (curent_row['Wins'] + curent_row['Loses']) / curent_row['Matches'] )
        ratio_draw.append(1 - ratio_win_lose[i])
        average_points_per_game.append( ((3 * ratio_win_lose[i]) + (2 * ratio_draw[i])) )


        alpha = curent_row['GoalsScored'] / curent_row['Matches']
        alpha = pow(alpha, gamma_coeficient)
        beta = curent_row['GoalsReceived'] / curent_row['Matches']
        beta = pow(beta, gamma_coeficient)
        beta = alpha + beta


        #aici inmultesc formula cu media golurilor pe meci cu APPG
        alpha = alpha * average_points_per_game[i]
        alpha = alpha / beta
        alpha *= curent_row['Matches']
        alpha = int(alpha)
        pythagorean_expectation.append(alpha)
        #print('PE = ', pythagorean_expectation[i])

    df_to_analyze['Expected Points'] = pythagorean_expectation

    return df_to_analyze.size, pythagorean_expectation,df_to_analyze['Points']



    #print(df_to_analyze)

def calculate_rmse(comparables_list, number_of_elements):
    rmse_value = 0
    # Calulam RMSE pentru gama ales
    for predicted_val, actual_val in comparables_list:
            rmse_value += pow((predicted_val - actual_val), 2)

    rmse_value /= number_of_elements  # de verificat daca asta chiar ia dimensiunea setului, daca functioneaza ca un len
    rmse_value = math.sqrt(rmse_value)
    

def calculate_rmse_avg(rmse_value):
    return statistics.mean(rmse_value)



if __name__ == '__main__':
    #generate_formula_for_all_teams('la liga', 2021)


