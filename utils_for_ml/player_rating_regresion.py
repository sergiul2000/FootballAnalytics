from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import math

# dataframes
import pandas as pd
# computation
import numpy as np
# visualization
import matplotlib.pyplot as plt
# import xgboost as xgb


def plot_prediction_vs_true_values(y_true, y_pred, title='train'):
    #On Train
    plt.figure(figsize=(10,10))
    plt.scatter(y_true, y_pred, c = 'crimson')
    plt.yscale('log')
    plt.xscale('log')

    p1 = max(max(y_pred), max(y_true))
    p2 = min(min(y_pred), min(y_true))
    
    plt.xlabel('True Values', fontsize=15)
    plt.ylabel('Predictions', fontsize=15)
    plt.axis('equal')
    plt.title(f"TrueVSPred for {title}")
    plt.plot([p1, p2], [p1, p2], 'b-')


df = pd.read_csv('utils_for_ml/unified_teams.csv')
# print(df.sample(n=15))

X = df[
    ['start_games', 'sub_games', 'mins', 'goals', 'assists', 'shot_per_game', 'offsides_per_game', 'total_shots',
     'fouls_per_game', 'total_fouls', 'yellow_cards', 'red_cards', 'clean_sheets', 'points', 'xG',
     'xA']].values  # ,'mapped_position','number_of_positions']].values
y = df['rating'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 20, test_size = 0.25, shuffle = True)


# degree = 3
# poly_model = PolynomialFeatures(degree = degree)

# poly_x_values = poly_model.fit_transform(X_train)

# print(f'initial values {X_train[0]}\nMapped to {poly_x_values[0]}')

# poly_model.fit(poly_x_values, y_train)

#HYPER PARAMETER TUNNING PE ASTA
DT_regressor = DecisionTreeRegressor(max_depth = 20, min_samples_leaf = 20, ccp_alpha=0.0001).fit(X_train, y_train)
y_pred = DT_regressor.predict(X_train)  # Predictions on Train Data
# print(y_pred)
# print(df['rating'])

#On Train
mean_squared_error(y_train, y_pred, squared=False)
MSE = np.square(np.subtract(y_train,y_pred)).mean()

RMSE = math.sqrt(MSE)
print(f'RMSE for Decision Tree Regresor on Train: {RMSE}')

print('Accuracy on train')
print(DT_regressor.score(X_train, y_train))

#plot_prediction_vs_true_values(y_train, y_pred, 'train')


#On test
y_pred_test = DT_regressor.predict(X_test)  # Predictions on Testing data

mean_squared_error(y_test, y_pred_test, squared = False)
MSE = np.square(np.subtract(y_test,y_pred_test)).mean()

RMSE = math.sqrt(MSE)
print(f'RMSE for Decision Tree Regresor on Train: {RMSE}')

print('Accuracy on test')
print(DT_regressor.score(X_test, y_test))



#plot_prediction_vs_true_values(y_test, y_pred_test, 'test')

# DT_regressor.plot_prediction_vs_true_values(y_pred)
# DT_regressor.plot_prediction_vs_true_values(y_pred_test)


#plot_prediction_vs_true_values(y_train, y_pred, 'train')
#plot_prediction_vs_true_values(y_test, y_test, 'test')
plt.show()

# TODO: K-fold Validation 
# TODO: Polynomial Regressor
# TODO: RandomForest Regressor
# TODO: XGBoost Regressor
# TODO: Plot each regressor both for train and for test




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
