from nturl2path import url2pathname
import plotly.graph_objects as go

#
import time
import numpy as np
import pandas as pd





def radar_plot_for_one_player(player_name, player_stats):
  
  name_fig = f'{player_name} stats'

  categories = ['goals', 'rating', 'age', 'assists', 'start games']
  
  fig = go.Figure()
  
  fig.add_trace(go.Scatterpolar(
      r = player_stats,
      theta = categories,
      fill = 'toself',
      name = name_fig
  ))

  fig.update_layout(
    polar=dict(
      radialaxis = dict(
        visible = True,
        range = [0, 50]
      )),
    showlegend = False
  )

  fig.update_layout(title_text = name_fig, title_x = 0.5)

  fig.show()


def radar_plot_for_comparing_two_players(player_name_1, player_stats_1,player_name_2, player_stats_2):
  
  name_fig_1= f'{player_name_1} stats'
  name_fig_2= f'{player_name_2} stats'
  fig_title = f'{name_fig_1} vs {name_fig_2}'
  
  categories = ['goals','rating','age', 'assists', 'start games']
  
  fig = go.Figure()
  
  fig.add_trace(go.Scatterpolar(
      r = player_stats_1,
      theta = categories,
      fill = 'toself',
      name = name_fig_1
  ))

  fig.add_trace(go.Scatterpolar(
      r = player_stats_2,
      theta = categories,
      fill = 'toself',
      name = name_fig_2
  ))

  fig.update_layout(
    polar = dict(
      radialaxis = dict(
        visible = True,
        range = [0, 50]
      )),
    showlegend=False
  )

  fig.update_layout(title_text = fig_title, title_x = 0.5)

  fig.show()


if __name__ == '__main__':
  #radar_plot_for_one_player("JORJ STELARUL",[1,3,4,2,5])
  barcelona = pd.read_csv('Barcelona.csv')
  print(barcelona.head(5))

  barcelona_selected = barcelona[['name', 'goals', 'rating', 'age', 'assists', 'start_games']]
  

  first_player_row = barcelona_selected.iloc[0].values.flatten().tolist()
  print(first_player_row[1:])


  radar_plot_for_one_player(first_player_row[0], first_player_row[1:])

  second_player_row = barcelona_selected.iloc[1].values.flatten().tolist()
  print(second_player_row[1:])


  radar_plot_for_comparing_two_players(first_player_row[0], first_player_row[1:],second_player_row[0], second_player_row[1:])

  
  