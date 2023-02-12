# from sklearn import __all__
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import KFold, train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from numpy import mean
from numpy import absolute
from numpy import sqrt
# from sklearn.tree import DecisionTreeRegressor
import math

# dataframes
import pandas as pd
# computation
import numpy as np
# visualization
import matplotlib.pyplot as plt
# import xgboost as xgb
from sklearn.tree import DecisionTreeRegressor


def plot_prediction_vs_true_values(y_true, y_pred, title='train'):
    # On Train
    plt.figure(figsize=(10, 10))
    plt.scatter(y_true, y_pred, c='crimson')
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

x = df[
    ['start_games', 'sub_games', 'mins', 'goals', 'assists', 'shot_per_game', 'offsides_per_game', 'total_shots',
     'fouls_per_game', 'total_fouls', 'yellow_cards', 'red_cards', 'clean_sheets', 'points', 'xG',
     'xA']].values  # ,'mapped_position','number_of_positions']].values
y = df['rating'].values

x_train, x_test, y_train, y_test = train_test_split(
    x, y, random_state=20, test_size=0.25, shuffle=True)


# degree = 3
# poly_model = PolynomialFeatures(degree = degree)

# poly_x_values = poly_model.fit_transform(X_train)

# print(f'initial values {X_train[0]}\nMapped to {poly_x_values[0]}')

# poly_model.fit(poly_x_values, y_train)

# HYPER PARAMETER TUNNING PE ASTA

############################################################################################################
# Decision Tree
DT_regressor = DecisionTreeRegressor(
    max_depth=20, min_samples_leaf=20, ccp_alpha=0.0001).fit(x_train, y_train)
y_pred_dt = DT_regressor.predict(x_train)  # Predictions on Train Data
# print(y_pred)
# print(df['rating'])

# On Train
mean_squared_error(y_train, y_pred_dt, squared=False)
MSE = np.square(np.subtract(y_train, y_pred_dt)).mean()

RMSE = math.sqrt(MSE)
print(f'RMSE for Decision Tree Regresor on Train: {RMSE}')

print('Accuracy on train')
print(DT_regressor.score(x_train, y_train))

# plot_prediction_vs_true_values(y_train, y_pred, 'train')


# On test
y_pred_test = DT_regressor.predict(x_test)  # Predictions on Testing data

mean_squared_error(y_test, y_pred_test, squared=False)
MSE = np.square(np.subtract(y_test, y_pred_test)).mean()

RMSE = math.sqrt(MSE)
print(f'RMSE for Decision Tree Regresor on Test: {RMSE}')

print('Accuracy on test')
print(DT_regressor.score(x_test, y_test))
print()

plot_prediction_vs_true_values(y_test, y_pred_test, 'test')

# DT_regressor.plot_prediction_vs_true_values(y_pred)
# DT_regressor.plot_prediction_vs_true_values(y_pred_test)


# plot_prediction_vs_true_values(y_train, y_pred, 'train')
# plot_prediction_vs_true_values(y_test, y_test, 'test')
# plt.show()

# Done TODO: K-fold Validation
# TODO: Polynomial Regressor
# Done TODO: RandomForest Regressor
# TODO: XGBoost Regressor
# TODO: Plot each regressor both for train and for test


############################################################################################################
# RandomForest
RF_regressor = RandomForestRegressor(n_estimators=100, random_state=0)

RF_regressor.fit(x_train, y_train)

Y_pred_rf = RF_regressor.predict(x_train)


mean_squared_error(y_train, Y_pred_rf, squared=False)
MSE = np.square(np.subtract(y_train, Y_pred_rf)).mean()

RMSE = math.sqrt(MSE)
print(f'RMSE for Random Forest on Train: {RMSE}')


print('Accuracy on train')
print(RF_regressor.score(x_train, y_train))


# On test
y_pred_test = RF_regressor.predict(x_test)  # Predictions on Testing data

mean_squared_error(y_test, y_pred_test, squared=False)
MSE = np.square(np.subtract(y_test, y_pred_test)).mean()

RMSE = math.sqrt(MSE)
print(f'RMSE for Decision Tree Regresor on Test: {RMSE}')

print('Accuracy on test')
print(RF_regressor.score(x_test, y_test))
print()

############################################################################################################
# K-fold Validation

# define cross-validation method to use
crossValidation = KFold(n_splits=10, random_state=1, shuffle=True)

# use k-fold CV to evaluate model
score_dt = cross_val_score(DT_regressor, x, y, scoring='neg_mean_squared_error',
                           cv=crossValidation, n_jobs=-1)
score_rf = cross_val_score(RF_regressor, x, y, scoring='neg_mean_squared_error',
                           cv=crossValidation, n_jobs=-1)

# view RMSE
RMSE = sqrt(mean(absolute(score_dt)))
print(f'RMSE for K-fold validation with Decision Tree model: {RMSE}')
RMSE = sqrt(mean(absolute(score_rf)))
print(f'RMSE for K-fold validation with Random forest model: {RMSE}')


############################################################################################################
# Polynomial Regressor


lin = LinearRegression()
lin.fit(x_train, y_train)

poly = PolynomialFeatures(degree=4)
X_poly_train = poly.fit_transform(x_train)

poly.fit(X_poly_train, y_train)
P_Regressor = LinearRegression()
P_Regressor.fit(X_poly_train, y_train)

y_pred_pr = P_Regressor.predict(X_poly_train)

mean_squared_error(y_train, y_pred_pr, squared=False)
MSE = np.square(np.subtract(y_train, y_pred_pr)).mean()

RMSE = math.sqrt(MSE)
print(f'RMSE for Polinomyal regressor on Train: {RMSE}')


print('Accuracy on train')

# de aici nu mai merge
# print(P_Regressor.score(poly.fit_transform(x_train), poly.fit_transform(y_train)))


# # On test
# y_pred_test = P_Regressor.predict(x_test)  # Predictions on Testing data

# mean_squared_error(y_test, y_pred_test, squared=False)
# MSE = np.square(np.subtract(y_test, y_pred_test)).mean()

# RMSE = math.sqrt(MSE)
# print(f'RMSE for Polynomial Regresor on Test: {RMSE}')

# print('Accuracy on test')
# print(P_Regressor.score(x_test, y_test))
# print()
