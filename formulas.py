import pandas as pd
from math import exp,pow

pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None  

from math import gamma, exp, sqrt
import statistics


def compute_extended_pythagorean_for_given_goal(given_goals, alphaGS_prim, alphaGA_prim, K, y, is_win):
    if is_win:
        a = (K * (given_goals + 1)) / alphaGS_prim 
        a = (-1) * pow(a,y)
        a = exp(a)

        b = (K * given_goals) / alphaGS_prim
        b = (-1) * pow(b,y)
        b =  exp(b)

        first_term = b - a

        c = (K * given_goals) / alphaGA_prim
        c = (-1) * pow(c,y)
        c = exp(c)

        second_term = 1 - c

        return first_term * second_term
    else:

        a = (K * (given_goals+1)) / alphaGS_prim 
        a = (-1) * pow(a,y)
        a = exp(a)

        b = (K * given_goals) / alphaGS_prim
        b = (-1) * pow(b,y)
        b =  exp(b)

        first_term = a - b

        c = (K * (given_goals+1)) / alphaGA_prim
        c = (-1) * pow(c,y)
        c = exp(c)

        d = (K * given_goals) / alphaGA_prim
        d = (-1) * pow(d,y)
        d = exp(d)


        second_term = c - d

        return first_term * second_term


def compute_points_per_game_pythagorian_estimation(limit_for_goals_iteration, alpha_goals_scored, alpha_goals_scored_prim, alpha_goals_against, alpha_goals_against_prim, K, y):
    # compute_prob_2
    win_probability = sum(compute_extended_pythagorean_for_given_goal(goal, alpha_goals_scored_prim, alpha_goals_against_prim, K, y,True) for goal in range(0,limit_for_goals_iteration ))
    draw_probability = sum(compute_extended_pythagorean_for_given_goal(goal, alpha_goals_scored_prim, alpha_goals_against_prim, K, y,False) for goal in range(0,limit_for_goals_iteration ))

    # 3 points for win
    # 1 point for draw
    print("")
    print(f"WIN PROB {win_probability} ")
    print(f"DRAW PROB {draw_probability*10} ")

    return (3 * win_probability) + (10 * draw_probability) , win_probability, draw_probability*10


def calculate_rmse(comparables_list, number_of_elements):
    rmse_value = 0
    # Calulam RMSE pentru gama ales
    for predicted_val, actual_val in comparables_list:
            rmse_value += pow((predicted_val - actual_val), 2)

    rmse_value /= number_of_elements  # de verificat daca asta chiar ia dimensiunea setului, daca functioneaza ca un len
    rmse_value = sqrt(rmse_value)
    return rmse_value


def calculate_rmse_avg(rmse_value):
    return statistics.mean(rmse_value)


def compute_pythagorian_expectation(df_to_analyze, gamma_coeficient):

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

    df_to_analyze[f'Expected Points y = {gamma_coeficient}'] = pythagorean_expectation

    return  df_to_analyze, pythagorean_expectation


def merge_lists(list1, list2):

    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list


