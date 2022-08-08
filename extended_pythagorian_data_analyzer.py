import pandas as pd
from math import exp,pow

pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None  

from math import gamma, exp


def compute_prob_1(c,alphaGS,alphaGA,y,is_win):
    if is_win:
        first_exp = (c +1)/alphaGS
        first_exp = pow(first_exp,y)
        first_exp = exp(first_exp)

        second_exp = c/alphaGS
        second_exp = -pow(second_exp,y)
        second_exp = exp(second_exp)

        first_term = first_exp - second_exp

        third_exp = c/alphaGA
        third_exp = -pow(third_exp,y)
        third_exp = exp(third_exp)

        second_term = 1 - third_exp

        print(f'Win {c} First term {first_term} Second_term {second_term}')
        return first_term * second_term
    else:
        first_exp = (c +1)/alphaGS
        first_exp = pow(first_exp,y)
        first_exp = exp(first_exp)

        second_exp = c/alphaGS
        second_exp = -pow(second_exp,y)
        second_exp = exp(second_exp)

        first_term = first_exp - second_exp

        third_exp = (c+1)/alphaGA
        third_exp = -pow(third_exp,y)
        third_exp = exp(third_exp)

        fourth_exp = (c)/alphaGA
        fourth_exp = -pow(fourth_exp,y)
        fourth_exp = exp(fourth_exp)

        second_term = third_exp - fourth_exp

        print(f'Draw {c} First term {first_term} Second_term {second_term}')
        return first_term * second_term

def compute_pythagorean_probability(number_of_goals, alpha_goals_scored_prim, alpha_goals_against_prim,K, y, is_win):
    if is_win:
        print('________________________________________________________________________________________________________________________________')
        print(f'WIN')
        print("")
        first_exp = (K * (number_of_goals + 1))/alpha_goals_scored_prim
        # print(f'FIRST K {first_exp}')
        first_exp = (-1) * pow(first_exp, y)
        # print(f'FIRST POW {first_exp}')
        first_exp = exp(first_exp)
        # print(f'FIRST EXP {first_exp}')
        # print('')
        
        second_exp = K * (number_of_goals)/alpha_goals_scored_prim
        # print(f'SECOND K {second_exp}')
        second_exp = (-1) * pow(second_exp,y)
        # print(f'SECOND POW {second_exp}')
        second_exp = exp(second_exp)
        # print(f'SECOND EXP {second_exp}')
        # print('')

        # second_exp scoatel si vezi daca merge
        first_term = first_exp - second_exp

        third_exp = K * (number_of_goals)/alpha_goals_against_prim
        # print(f'THIRD K {third_exp}')
        third_exp = (-1) * pow(third_exp, y)
        # print(f'THIRD POW {third_exp}')
        third_exp = 1 - exp(third_exp)
        # print(f'THIRD EXP {third_exp}')
        # print('')

        second_term  = third_exp

        return_val = first_term * second_term

        
        print(f'1st {first_exp} 2nd {second_exp} 3rd {third_exp}')
        print(f'1st {first_term} 2nd {second_term}')
        print(f'Return Value {return_val}')

        return return_val
    else:
        print('________________________________________________________________________________________________________________________________')
        print('DRAW')
        print('')
        first_exp = (K * (number_of_goals + 1))/alpha_goals_scored_prim
        #print(f'FIRST K {first_exp}')
        first_exp = (-1) * pow(first_exp,y)
        #print(f'FIRST POW {first_exp}')
        first_exp = exp(first_exp)
        #print(f'FIRST EXP {first_exp}')
        #print('')

        second_exp = K * (number_of_goals)/alpha_goals_scored_prim
        #print(f'SECOND K {second_exp}')
        second_exp = (-1) * pow(second_exp,y)
        #print(f'SECOND POW {second_exp}')
        second_exp = exp(second_exp)
        #print(f'SECOND EXP {second_exp}')
        #print('')

        # second_exp scoatel si vezi daca merge
        first_term = first_exp - second_exp
        

        third_exp = (K * (number_of_goals + 1))/alpha_goals_against_prim
        #print(f'THIRD K {third_exp}')
        third_exp = (-1) * pow(third_exp,y)
        #print(f'THIRD POW {third_exp}')
        third_exp = exp(third_exp)
        #print(f'THIRD EXP {third_exp}')
        #print('')


        fourth_exp = K * (number_of_goals)/alpha_goals_against_prim
        # print(f'FOURTH K {fourth_exp}')
        fourth_exp = (-1) * pow(fourth_exp, y)
        # print(f'FOURTH POW {fourth_exp}')
        fourth_exp = exp(fourth_exp)
        # print(f'FOURTH EXP {fourth_exp}')
        # print('')


        second_term = third_exp - fourth_exp
        
        return_val = first_term * second_term

        print(f'1st {first_exp} 2nd {second_exp} 3rd {third_exp} 4th {fourth_exp}')
        print(f'1st {first_term} 2nd {second_term}')
        print(f'Return Value {return_val}')

        return return_val

def compute_pythagorean_probability_for_given_goals(number_of_goals, alpha_goals_scored, alpha_goals_against, pythagorian_exponent, is_win):
    if is_win:
        first_element = exp(-pow(((number_of_goals+1)/alpha_goals_scored), pythagorian_exponent)) - exp(-pow(((number_of_goals)/alpha_goals_scored),pythagorian_exponent))
        second_element = 1 - exp(-pow((number_of_goals)/alpha_goals_against ,pythagorian_exponent))

        print(f'Win First {first_element} Second {second_element} MUL {second_element * first_element}')

        return first_element * second_element
    else:
        first_element =  exp(-pow(((number_of_goals+1)/alpha_goals_scored),pythagorian_exponent)) - exp(-pow(((number_of_goals)/alpha_goals_scored),pythagorian_exponent))
        second_element = exp(-pow(((number_of_goals+1)/alpha_goals_against) ,pythagorian_exponent)) - exp(-pow(((number_of_goals)/alpha_goals_against) ,pythagorian_exponent))
        
        print(f'Draw First {first_element} Second {second_element}') 
        return first_element * second_element

def compute_prob_2(c, alphaGS_prim, alphaGA_prim, K, y, is_win):
    if is_win:
        a = (K * (c+1)) / alphaGS_prim 
        a = (-1) * pow(a,y)
        a = exp(a)

        b = (K * c) / alphaGS_prim
        b = (-1) * pow(b,y)
        b =  exp(b)

        first_term = b - a

        c = (K * c) / alphaGA_prim
        c = (-1) * pow(c,y)
        c = exp(c)

        second_term = 1 - c

        return first_term * second_term
    else:

        a = (K * (c+1)) / alphaGS_prim 
        a = (-1) * pow(a,y)
        a = exp(a)

        b = (K * c) / alphaGS_prim
        b = (-1) * pow(b,y)
        b =  exp(b)

        first_term = a - b

        c1 = (K * (c+1)) / alphaGA_prim
        c1 = (-1) * pow(c1,y)
        c1 = exp(c1)

        d = (K * c) / alphaGA_prim
        d = (-1) * pow(d,y)
        d = exp(d)


        second_term = c1 - d

        return first_term * second_term



def compute_points_per_game_pythagorian_estimation(limit_for_goals_iteration, alpha_goals_scored, alpha_goals_scored_prim, alpha_goals_against, alpha_goals_against_prim, K, pythagorian_exponent):
    # compute_prob_2
    win_probability = sum(compute_prob_2(goal, alpha_goals_scored_prim, alpha_goals_against_prim, K, pythagorian_exponent,True) for goal in range(0,limit_for_goals_iteration ))
    draw_probability = sum(compute_prob_2(goal, alpha_goals_scored_prim, alpha_goals_against_prim, K, pythagorian_exponent,False) for goal in range(0,limit_for_goals_iteration ))

    # 3 points for win
    # 1 point for draw
    print("")
    print(f"WIN PROB {win_probability} ")
    print(f"DRAW PROB {draw_probability*10} ")

    return (3 * win_probability) + (10*draw_probability) , win_probability, draw_probability*10

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
    # print(f"SKEWNESS {y}")
    
    K = gamma(1+(1/y))
    # print(f"K {K}")



    df_to_analyze['AvgGS'] = df_to_analyze['GoalsScored']/df_to_analyze['Matches']
    df_to_analyze['AvgGA'] = df_to_analyze['GoalsReceived']/df_to_analyze['Matches']

    #alpha GS
    df_to_analyze['alphaGS'] = df_to_analyze['GoalsScored'].apply(lambda GS: round((GS-beta)/K),2)
    #alpha GR
    df_to_analyze['alphaGA'] = df_to_analyze['GoalsReceived'].apply(lambda GA: round((GA-beta)/K),2)

    # alpha GS * K
    df_to_analyze['alphaGGS'] = df_to_analyze['alphaGS'].apply(lambda alphaGS: round(alphaGS * K,2) )
    #alpha GR * K
    df_to_analyze['alphaGGA'] = df_to_analyze['alphaGA'].apply(lambda alphaGA: round(alphaGA * K,2) )


    # df_to_analyze['AvgGS_Int'] = df_to_analyze['AvgGA'].astype('int')
    # df_to_analyze['AvgGA_Int'] = df_to_analyze['AvgGA'].astype('int')

    for index,row in df_to_analyze.iterrows():
        #print(row)
        
        points_per_game_expectancy, win_expectancy, draw_expectancy = compute_points_per_game_pythagorian_estimation(1000, row['alphaGS'],row['alphaGGS'], row['alphaGA'], row['alphaGGA'],K ,y)
        points = int(row['Matches'] * points_per_game_expectancy)
        win_expectancy = int(row['Matches'] * win_expectancy)
        draw_expectancy = int(row['Matches'] * draw_expectancy) +1
        lose_expectancy = row['Matches'] - int(win_expectancy) - (int(draw_expectancy))

        df_to_analyze.at[index,'Estimated_Wins'] = win_expectancy
        df_to_analyze.at[index,'Estimated_Draws'] = draw_expectancy
        df_to_analyze.at[index,'Estimated_Loses'] = lose_expectancy
        df_to_analyze.at[index,'Estimated_Points_Extended'] =  points


    df_to_analyze['Delta_Points_Extended'] = df_to_analyze['Points'] - df_to_analyze['Estimated_Points_Extended']

    print(df_to_analyze)


    df_to_save= df_to_analyze[['Team','Matches','Wins','Draws','Loses','GoalsScored', 'GoalsReceived', 'Points','Estimated_Wins', 'Estimated_Draws', 'Estimated_Loses', 'Estimated_Points_Extended','Delta_Points_Extended']]
    df_to_save.to_csv("initial_report.csv")



    # df_to_analyze['Win_Pythagorean'] = sum(exp(total_goal) for total_goal in range(0, df_to_analyze['AvgGS_Int']))
    # df_to_analyze['Draw_Pythagorean'] =
    # print(df_to_analyze['Win_Pythagorean'])

    # df_to_analyze['Points_Pythagorean'] = (3 * df_to_analyze['Win_Probability'])+ df_to_analyze['Draw_Probability']
    
    
    # c variaza numarul de goluri 0, N



    #print(df_to_analyze)





if __name__ == '__main__':
    # print(sum(20*i for i in range(100, 200)))

    apply_pythagorian_league_table_stats('la liga', 2015)
    # for year in range(2014,2022):
    #     print(f'{year} - {year+1}')
    #     apply_pythagorian_league_table_stats('bundesliga',year)