import plotly.graph_objects as go
import pandas as pd
import plotly.figure_factory as ff


path = f'dataframes/league_table/la liga/la liga_league_table_in_season_2015_2016.csv'

df = pd.read_csv(path)

dx = df['Team']
dy1 = df['G']
dy2 = df['GA']


def create_figure(data_frame, data_x_axis, data_y1_axis, data_y2_axis, data_y3_axis, title, y_column_name, blue_line_name, black_line_name, amber_line_name):


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

if __name__ == '__main__':
    # create_figure('123', dx, dy1, dy2)
    create_figure(df, df['Team'], df['G'], df['GA'], df['W'], 'Goals difference', 'Goals123', 'Goluri date', 'Goluri luate','Wins')