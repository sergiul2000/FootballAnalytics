from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor

# dataframes
import pandas as pd
# computation
import numpy as np
# visualization
import matplotlib.pyplot as plt
# import xgboost as xgb

df = pd.read_csv('leverskusen_2014_2015_rating.csv')
# print(df.sample(n=15))

x_values = df[
    ['start_games', 'sub_games', 'mins', 'goals', 'assists', 'shot_per_game', 'offsides_per_game', 'total_shots',
     'fouls_per_game', 'total_fouls', 'yellow_cards', 'red_cards', 'clean_sheets', 'points', 'xG',
     'xA']].values  # ,'mapped_position','number_of_positions']].values
y_values = df['rating'].values

# print(x_values[0], y_values[0])
degree = 3
poly_model = PolynomialFeatures(degree=degree)

poly_x_values = poly_model.fit_transform(x_values)

print(f'initial values {x_values[0]}\nMapped to {poly_x_values[0]}')

poly_model.fit(poly_x_values, y_values)

DT_model = DecisionTreeRegressor(max_depth=5).fit(x_values, y_values)
DT_predict = DT_model.predict(x_values)  # Predictions on Testing data
print(DT_predict)
print(df['rating'])

# we use linear regression as a base!!! ** sometimes misunderstood **
# regression_model = LinearRegression()

# regression_model.fit(poly_x_values, y_values)

# y_pred = regression_model.predict(poly_x_values)

# regression_model.coef_

# mean_squared_error(y_values, y_pred, squared=False)

# check our accuracy for each degree, the lower the error the better!
# number_degrees = [1,2,3,4,5,6,7]
# plt_mean_squared_error = []
# for degree in number_degrees:

#    poly_model = PolynomialFeatures(degree=degree)

#    poly_x_values = poly_model.fit_transform(x_values)
#    poly_model.fit(poly_x_values, y_values)

#    regression_model = LinearRegression()
#    regression_model.fit(poly_x_values, y_values)
#    y_pred = regression_model.predict(poly_x_values)

#    plt_mean_squared_error.append(mean_squared_error(y_values, y_pred, squared=False))

# plt.scatter(number_degrees,plt_mean_squared_error, color="green")
# plt.plot(number_degrees,plt_mean_squared_error, color="red")
