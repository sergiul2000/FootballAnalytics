# from sklearn import __all__
from xgboost import XGBRegressor
from sklearn import ensemble
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

from my_logger import logger


def plot_prediction_vs_true_values(y_true, y_pred, title):
    # On Train
    plt.figure(figsize=(10, 10))
    plt.scatter(y_true, y_pred, c="crimson")
    plt.yscale("log")
    plt.xscale("log")

    p1 = max(max(y_pred), max(y_true))
    p2 = min(min(y_pred), min(y_true))

    plt.xlabel("True Values", fontsize=15)
    plt.ylabel("Predictions", fontsize=15)
    plt.axis("equal")
    plt.title(f"True VS Pred for {title}")
    plt.plot([p1, p2], [p1, p2], "b-")
    plt.show()


def plot_polynomial_regression(y_true, y_pred, title):
    plt.scatter(y_true, y_pred, color="blue")

    lin2 = LinearRegression()
    plt.plot(y_pred, lin2.predict(poly.fit_transform(y_true)), color="red")
    plt.title("Polynomial Regression")
    plt.xlabel("True values")
    plt.ylabel("Predicted values")

    plt.show()


my_logger = logger(
    "D:\\aaLicenta\\licenta\FootballAnalytics\\utils_for_ml\\logs_of_player_rating_regresion.txt"
)

my_logger.print_logs_in_file("start")

df = pd.read_csv("utils_for_ml/unified_players.csv")
# print(df.sample(n=15))
df_player_rating_predictions = pd.DataFrame()

x = df[
    [
        "start_games",
        "sub_games",
        "mins",
        "goals",
        "assists",
        "shot_per_game",
        "offsides_per_game",
        "total_shots",
        "fouls_per_game",
        "total_fouls",
        "yellow_cards",
        "red_cards",
        "clean_sheets",
        "points",
        "xG",
        "xA",
    ]
].values  # ,'mapped_position','number_of_positions']].values
y = df["rating"].values

x_train, x_test, y_train, y_test = train_test_split(
    x, y, random_state=20, test_size=0.25, shuffle=True
)

# df_player_rating_predictions['name'] = x_test['name'].values
# print(x_test)

df_id = df["player_number"][-1129:]
df_names = df["name"][-1129:]
df_year_start = df["year_start"][-1129:]
df_year_end = df["year_end"][-1129:]
df_player_rating_predictions["player_number"] = df_id.values
df_player_rating_predictions["name"] = df_names.values
df_player_rating_predictions["Year_start"] = df_year_start.values
df_player_rating_predictions["Year_end"] = df_year_end.values
df_player_rating_predictions["Test points"] = y_test


# degree = 3
# poly_model = PolynomialFeatures(degree = degree)

# poly_x_values = poly_model.fit_transform(X_train)

# print(f'initial values {X_train[0]}\nMapped to {poly_x_values[0]}')

# poly_model.fit(poly_x_values, y_train)

# HYPER PARAMETER TUNNING PE ASTA

############################################################################################################
# Decision Tree
DT_regressor = DecisionTreeRegressor(
    max_depth=20, min_samples_leaf=20, ccp_alpha=0.0001
).fit(x_train, y_train)
y_pred_dt = DT_regressor.predict(x_train)  # Predictions on Train Data
# print(y_pred)
# print(df['rating'])

# On Train
mean_squared_error(y_train, y_pred_dt, squared=False)
MSE = np.square(np.subtract(y_train, y_pred_dt)).mean()

RMSE = math.sqrt(MSE)
my_logger.print_logs_in_file(f"RMSE for Decision Tree Regresor on Train: {RMSE}")

my_logger.print_logs_in_file("Accuracy on train")
my_logger.print_logs_in_file(str(DT_regressor.score(x_train, y_train)))

plot_prediction_vs_true_values(y_train, y_pred_dt, "train Decision Tree regressor")


# On test
y_pred_test = DT_regressor.predict(x_test)  # Predictions on Testing data

mean_squared_error(y_test, y_pred_test, squared=False)
MSE = np.square(np.subtract(y_test, y_pred_test)).mean()

RMSE = math.sqrt(MSE)
my_logger.print_logs_in_file(f"RMSE for Decision Tree Regresor on Test: {RMSE}")

my_logger.print_logs_in_file("Accuracy on test")
my_logger.print_logs_in_file(str(DT_regressor.score(x_test, y_test)))
my_logger.print_logs_in_file("")

plot_prediction_vs_true_values(y_test, y_pred_test, "test Decision Tree regressor")
df_player_rating_predictions["Decision tree points"] = y_pred_test


# DT_regressor.plot_prediction_vs_true_values(y_pred)
# DT_regressor.plot_prediction_vs_true_values(y_pred_test)


# plot_prediction_vs_true_values(y_train, y_pred, 'train')
# plot_prediction_vs_true_values(y_test, y_test, 'test')
# plt.show()

# Done TODO: K-fold Validation
# Done (without plotting) TODO: Polynomial Regressor
# Done TODO: RandomForest Regressor
# Done TODO: XGBoost Regressor
# Done TODO: Plot each regressor both for train and for test


############################################################################################################
# RandomForest
RF_regressor = RandomForestRegressor(n_estimators=100, random_state=0)

RF_regressor.fit(x_train, y_train)

Y_pred_rf = RF_regressor.predict(x_train)


mean_squared_error(y_train, Y_pred_rf, squared=False)
MSE = np.square(np.subtract(y_train, Y_pred_rf)).mean()

RMSE = math.sqrt(MSE)
my_logger.print_logs_in_file(f"RMSE for Random Forest on Train: {RMSE}")


my_logger.print_logs_in_file("Accuracy on train")
my_logger.print_logs_in_file(str(RF_regressor.score(x_train, y_train)))

plot_prediction_vs_true_values(y_train, y_pred_dt, "train Random Forest regressor")

# On test
y_pred_test = RF_regressor.predict(x_test)  # Predictions on Testing data

mean_squared_error(y_test, y_pred_test, squared=False)
MSE = np.square(np.subtract(y_test, y_pred_test)).mean()

RMSE = math.sqrt(MSE)
my_logger.print_logs_in_file(f"RMSE for Random Forest on Test: {RMSE}")

my_logger.print_logs_in_file("Accuracy on test")
my_logger.print_logs_in_file(str(RF_regressor.score(x_test, y_test)))
my_logger.print_logs_in_file("")

plot_prediction_vs_true_values(y_test, y_pred_test, "test Random Forest regressor")

df_player_rating_predictions["Random forest points"] = y_pred_test

############################################################################################################
# XGBoost
# cu 100 de estimatoare merge cel mai bine
XGB_Regressor = XGBRegressor(
    n_estimators=100, max_depth=7, eta=0.1, subsample=0.7, colsample_bytree=0.8
).fit(x_train, y_train)
y_pred_xgb = XGB_Regressor.predict(x_train)  # Predictions on Train Data


# On Train
mean_squared_error(y_train, y_pred_xgb, squared=False)
MSE = np.square(np.subtract(y_train, y_pred_xgb)).mean()

RMSE = math.sqrt(MSE)
my_logger.print_logs_in_file(f"RMSE for XGBoost Regresor on Train: {RMSE}")

my_logger.print_logs_in_file("Accuracy on train")
my_logger.print_logs_in_file(str(XGB_Regressor.score(x_train, y_train)))

plot_prediction_vs_true_values(y_train, y_pred_xgb, "train XGBoost regressor")


# On test
y_pred_test = XGB_Regressor.predict(x_test)  # Predictions on Testing data

mean_squared_error(y_test, y_pred_test, squared=False)
MSE = np.square(np.subtract(y_test, y_pred_test)).mean()

RMSE = math.sqrt(MSE)
my_logger.print_logs_in_file(f"RMSE for XGBoost Regresor on Test: {RMSE}")

my_logger.print_logs_in_file("Accuracy on test")
my_logger.print_logs_in_file(str(XGB_Regressor.score(x_test, y_test)))
my_logger.print_logs_in_file("")

plot_prediction_vs_true_values(y_test, y_pred_test, "test XGBoost regressor")


df_player_rating_predictions["XGBoost points"] = y_pred_test
############################################################################################################
# Polynomial Regressor


# lin = LinearRegression()
# lin.fit(x_train, y_train)

# On train

poly = PolynomialFeatures(degree=4)
X_poly_train = poly.fit_transform(x_train)
poly.fit(X_poly_train, y_train)

P_Regressor = LinearRegression()
P_Regressor.fit(X_poly_train, y_train)

y_pred_pr = P_Regressor.predict(X_poly_train)

mean_squared_error(y_train, y_pred_pr, squared=False)
MSE = np.square(np.subtract(y_train, y_pred_pr)).mean()

RMSE = math.sqrt(MSE)
my_logger.print_logs_in_file(f"RMSE for Polinomyal regressor on Train: {RMSE}")


my_logger.print_logs_in_file("Accuracy on train")
my_logger.print_logs_in_file(str(P_Regressor.score(X_poly_train, y_train)))

plot_prediction_vs_true_values(y_train, y_pred_pr, "train polynomial regressor")

# On test

X_poly_test = poly.fit_transform(x_test)
poly.fit(X_poly_test, y_test)


P_Regressor.fit(X_poly_test, y_test)

y_pred_test = P_Regressor.predict(X_poly_test)  # Predictions on Testing data

mean_squared_error(y_test, y_pred_test, squared=False)
MSE = np.square(np.subtract(y_test, y_pred_test)).mean()

RMSE = math.sqrt(MSE)
my_logger.print_logs_in_file(f"RMSE for Polynomial Regresor on Test: {RMSE}")

my_logger.print_logs_in_file("Accuracy on test")
my_logger.print_logs_in_file(str(P_Regressor.score(X_poly_test, y_test)))

my_logger.print_logs_in_file("")

plot_prediction_vs_true_values(y_test, y_pred_test, "test polynomial regressor")


df_player_rating_predictions["Polynomial points"] = y_pred_test
############################################################################################################
# K-fold Validation

# define cross-validation method to use
crossValidation = KFold(n_splits=10, random_state=1, shuffle=True)

# use k-fold CV to evaluate model
score_dt = cross_val_score(
    DT_regressor, x, y, scoring="neg_mean_squared_error", cv=crossValidation, n_jobs=-1
)
score_rf = cross_val_score(
    RF_regressor, x, y, scoring="neg_mean_squared_error", cv=crossValidation, n_jobs=-1
)
score_xgb = cross_val_score(
    XGB_Regressor, x, y, scoring="neg_mean_squared_error", cv=crossValidation, n_jobs=-1
)
score_poly = cross_val_score(
    P_Regressor, x, y, scoring="neg_mean_squared_error", cv=crossValidation, n_jobs=-1
)

# view RMSE
RMSE = sqrt(mean(absolute(score_dt)))
my_logger.print_logs_in_file(
    f"RMSE for K-fold validation with Decision Tree model: {RMSE}"
)

RMSE = sqrt(mean(absolute(score_rf)))
my_logger.print_logs_in_file(
    f"RMSE for K-fold validation with Random Forest model: {RMSE}"
)

RMSE = sqrt(mean(absolute(score_xgb)))
my_logger.print_logs_in_file(
    f"RMSE for K-fold validation with XGBoost Tree model: {RMSE}"
)

RMSE = sqrt(mean(absolute(score_poly)))
my_logger.print_logs_in_file(
    f"RMSE for K-fold validation with Polynomial Tree model: {RMSE}"
)
my_logger.print_logs_in_file("")


my_logger.print_logs_in_file("end")

df_player_rating_predictions.to_csv("./converted_files/player_rating_predictors.csv")
