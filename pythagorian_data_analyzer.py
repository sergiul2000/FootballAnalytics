import math
from platform import win32_edition
from sklearn.linear_model import LinearRegression
from math import gamma, exp
import pandas as pd
from math import exp, pow

import py
from pyparsing import java_style_comment
from pyrsistent import b
pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None


#def pythagorean_expectation(goals_scored, goals_conceded, average_points_per_game, pythagorean_expectation):

    #pythagorean_expectation var is the PE from the article
    #pythagorean_expectation = pow(goals_scored, ga)


def calculate_simple_linear_regression_league_table_stats(league, year):

    #TO DO: hard-codeaza liga a.i. sa poti sa iti aduci datele din toate ligile
    path = f'dataframes/league_table/{league}/{league}_league_table_in_season_{year}_{year + 1}.csv'

    df = pd.read_csv(path)
    frames =[df]
    for i in range(7):
        path = f'dataframes/league_table/{league}/{league}_league_table_in_season_{year + i}_{year + 1 + i}.csv'
        df_iterator_same_league_different_year = pd.read_csv(path)
        frames.append(df_iterator_same_league_different_year)
    df_result = pd.concat(frames)


    #df_to_analyze este un set de date intermediar unde luam doar cateva coloane din df care contine toate coloanele setului de date
    df_to_analyze = df_result[['Team', 'M', 'W', 'D', 'L', 'G', 'GA', 'PTS']]

    #pare sa fi mers, trebuie sa il intreb pe Dan daca le pune bine impreuna
    print(df_result)

    #redenumim coloanele pentru a avea nume mai sugestive
    df_to_analyze.rename(columns={'M': 'Matches',
                                  'W': 'Wins',
                                  'D': 'Draws',
                                  'L': 'Loses',
                                  'G': 'GoalsScored',
                                  'GA': 'GoalsReceived',
                                  'PTS': 'Points',
                                  }, inplace=True)

    set_antrenament = df_to_analyze['GoalsScored'].values.reshape(-1, 1)
    set_observat = df_to_analyze['Points'].values.reshape(-1, 1)

    linear_regresor = LinearRegression()
    linear_regresor.fit(set_antrenament, set_observat)

    points_predicted = linear_regresor.predict(set_antrenament)

    #transformam punctele in intregi, deoarece nu putem avea puncte zecimale. Insa eroarea e mai mica daca lasam zecimalele
    # for i in range(len(points_predicted)):
    #     points_predicted[i] = int(points_predicted[i])

    #printez punctele reale comparate cu punctele prezise de regresia lineara si se observa diferente foarte mari
    #print(df_to_analyze['Points'], points_predicted)

    z=0

    for i in set_antrenament:
        for j in points_predicted:
            z += pow((i-j), 2)

    z /= set_antrenament.size #de verificat daca asta chiar ia dimensiunea setului, daca functioneaza ca un len
    z = math.sqrt(z)

    print(z)

    #TO DO: antreneaza regresia pe mai multi ani si mai multe ligi. Setul de antrenament e prea mic

if __name__ == '__main__':
    calculate_simple_linear_regression_league_table_stats('la liga', 2015)
