from nturl2path import url2pathname
import plotly.graph_objects as go

#
import time
import numpy as np
import pandas as pd
import time
import pickle
import sys
from tqdm import tqdm
from selenium import webdriver

#

#
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)
driver.get('https:/1xbet.whoscored.com/')
driver.close()

#
def crawling_player_summary(team_id, api_delay_term=5):
    """
    crawling player statistics of certain team
    
    Args :
        team_id : team number 
        
    return :
        player statistics (dataframe)
    
    """

    # connect webdriver
    url = "https://www.whoscored.com/Teams/" + str(team_id)
    driver = webdriver.Chrome('C:/Users/Infosci_center/Desktop/soccer/chromedriver')
    driver.get(url)

    # wait for getting data
    time.sleep(api_delay_term)


categories = ['goals','rating','games',
              'age', 'asists']



fig = go.Figure()

fig.add_trace(go.Scatterpolar(
      r=[2,3,5,4,3]
      theta=categories,
      fill='toself',
      name='Product A'
))

# fig.add_trace(go.Scatterpolar(
#       r=[2, 4, 1, 5, 3],
#       theta=categories,
#       fill='toself',
#       name='Product b'
# ))

# fig.add_trace(go.Scatterpolar(
#       r=[3, 5, 4, 1, 2],
#       theta=categories,
#       fill='toself',
#       name='Product c'
# ))

# fig.add_trace(go.Scatterpolar(
#       r=[4, 2, 3, 1, 5],
#       theta=categories,
#       fill='toself',
#       name='Product d'
# ))

fig.add_trace(go.Scatterpolar(
      r=[5, 1, 2, 4, 3],
      theta=categories,
      fill='toself',
      name='Product e'
))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 5]
    )),
  showlegend=False
)

fig.show()

