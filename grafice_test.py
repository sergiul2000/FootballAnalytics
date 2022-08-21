import plotly.graph_objects as go
import pandas as pd
import plotly.figure_factory as ff
from formulas import *

path = f'dataframes/pythagorian_league_table/la liga/la liga_pythagorian_league_table_in_season_2014_2015.csv'

df = pd.read_csv(path)
df = df.drop(columns=['AvgGS', 'AvgGA', 'Estimated_Wins_Extended', 'Estimated_Draws_Extended', 'Estimated_Loses_Extended'])

# df = compute_pythagorian_expectation('la liga', 2021)

dx = df['Points']
estimated_simple_pyth = df['Estimated_Points_Simple']
estimated_extended_pyth = df['Estimated_Points_Extended']


def calculate_array_of_deltas_for_all_sezons():
    array_deltas_of_all_years_simple = []
    array_deltas_of_all_years_extended = []
    j = 0

    for i in range(2014, 2022):
        path = f'dataframes/pythagorian_league_table/la liga/la liga_pythagorian_league_table_in_season_{i}_{i+1}.csv'
        df_for_array =  pd.read_csv(path)
        df_for_array = df_for_array.drop(columns=['AvgGS', 'AvgGA', 'Estimated_Wins_Extended', 'Estimated_Draws_Extended',
                              'Estimated_Loses_Extended'])

        estimated_simple_pyth_local = df_for_array['Delta_Points_Simple']
        estimated_extended_pyth_local = df_for_array['Delta_Points_Extended']
        a, b = calculate_mean_deltas_of_one_year(estimated_simple_pyth_local, estimated_extended_pyth_local)
        array_deltas_of_all_years_simple.append(a)
        array_deltas_of_all_years_extended.append(b)

        j += 1

    return array_deltas_of_all_years_simple, array_deltas_of_all_years_extended



def calculate_mean_deltas_of_one_year(delta_points_simple, delta_points_extended):

    avg_delta_points_simple = 0
    avg_delta_points_extended = 0

    for i in delta_points_simple:
        avg_delta_points_simple += abs(i)

    for j in delta_points_extended:
        avg_delta_points_extended += abs(j)

    avg_delta_points_simple /= 19
    avg_delta_points_extended /= 19

    avg_delta_points_simple = round(avg_delta_points_simple,2)
    avg_delta_points_extended = round(avg_delta_points_extended,2)

    return avg_delta_points_simple, avg_delta_points_extended


def create_estimated_points_of_one_sezon_figure(data_frame, data_x_axis, data_y1_axis, data_y2_axis, data_y3_axis, title, y_column_name, blue_line_name, black_line_name, amber_line_name):

    # Initialize a figure with ff.create_table(table_data)
    fig = ff.create_table(data_frame, height_constant=60)


    # Make traces for graph
    trace1 = go.Bar(x=data_x_axis, y=data_y1_axis, xaxis='x2', yaxis='y2',
                    marker=dict(color='#E3B5A4'),
                    name=blue_line_name)
    trace2 = go.Bar(x=data_x_axis, y=data_y2_axis, xaxis='x2', yaxis='y2',
                    marker=dict(color='#E85F5C'),
                    name=black_line_name)
    trace3 = go.Bar(x=data_x_axis, y=data_y3_axis, xaxis='x2', yaxis='y2',
                    marker=dict(color='#773344'),
                    name=amber_line_name)

    # Add trace data to figure
    fig.add_traces([trace1, trace2,trace3])

    # initialize xaxis2 and yaxis2
    fig['layout']['xaxis2'] = {}
    fig['layout']['yaxis2'] = {}

    # Edit layout for subplots
    fig.layout.yaxis.update({'domain': [0, .45]})
    fig.layout.yaxis2.update({'domain': [.6, 1]})

    # The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
    fig.layout.yaxis2.update({'anchor': 'x2'})
    fig.layout.xaxis2.update({'anchor': 'y2'})
    fig.layout.yaxis2.update({'title': y_column_name})

    # Update the margins to add a title and see graph x-labels.
    fig.layout.margin.update({'t': 75, 'l': 50})
    fig.layout.update({'title': title})

    # Update the height because adding a graph vertically will interact with
    # the plot height calculated for the table
    fig.layout.update({'height': 800})

    # Plot!
    fig.show()


def create_avg_deltas_figure(data_frame, title, y_column_name, blue_line_name, black_line_name):
    sezons = ['2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
    array_of_simple_deltas, array_of_extended_deltas = calculate_array_of_deltas_for_all_sezons()
    # print(array_of_simple_deltas)
    # print(array_of_extended_deltas)

    # Initialize a figure with ff.create_table(table_data)
    fig = ff.create_table(data_frame, height_constant=60)


    # Make traces for graph
    trace1 = go.Bar(x=sezons, y=array_of_simple_deltas, xaxis='x2', yaxis='y2',
                    marker=dict(color='#E3B5A4'),
                    name=blue_line_name)
    trace2 = go.Bar(x=sezons, y=array_of_extended_deltas, xaxis='x2', yaxis='y2',
                    marker=dict(color='#E85F5C'),
                    name=black_line_name)

    # Add trace data to figure
    fig.add_traces([trace1, trace2])

    # initialize xaxis2 and yaxis2
    fig['layout']['xaxis2'] = {}
    fig['layout']['yaxis2'] = {}

    # Edit layout for subplots
    fig.layout.yaxis.update({'domain': [0, .45]})
    fig.layout.yaxis2.update({'domain': [.6, 1]})

    # The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
    fig.layout.yaxis2.update({'anchor': 'x2'})
    fig.layout.xaxis2.update({'anchor': 'y2'})
    fig.layout.yaxis2.update({'title': y_column_name})

    # Update the margins to add a title and see graph x-labels.
    fig.layout.margin.update({'t': 75, 'l': 50})
    fig.layout.update({'title': title})

    # Update the height because adding a graph vertically will interact with
    # the plot height calculated for the table
    fig.layout.update({'height': 800})

    # Plot!
    fig.show()

if __name__ == '__main__':
    # create_figure('123', dx, dy1, dy2)
    create_estimated_points_of_one_sezon_figure(df, df['Team'], dx, estimated_simple_pyth, estimated_extended_pyth, 'Estimated points by 2 formulas', 'Points', 'Points recorded', 'Points estimated by Simple Pythagorian method',
                  'Points estimted by Extended Pythagorian method')
    create_avg_deltas_figure(df, 'Estimated points by 2 formulas','Points', 'Average delta points with simple pithagoryan',
                                                'Average delta points with extended pithagoryan')
    # print(calculate_mean_deltas_of_one_year(df['Delta_Points_Simple'], df['Delta_Points_Extended']))
