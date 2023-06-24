# from sklearn import __all__
from xgboost import XGBRegressor

# import xgboost as xgb

from sklearn import ensemble
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import KFold, train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from numpy import mean
from numpy import absolute
from numpy import sqrt
from lazypredict.Supervised import LazyRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from joblib import dump

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


my_logger = logger(".\\utils_for_ml\\logs_of_player_rating_regresion.txt")

my_logger.print_logs_in_file("start")

df = pd.read_csv("utils_for_ml/unified_players.csv")
# print(df.sample(n=15))
df_player_rating_predictions = pd.DataFrame()
# print(df)
x = df[
    [
        "start_games",
        "sub_games",
        "mins",
        # "mapped_position",
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
]  # .values  # ,'mapped_position','number_of_positions']].values
y = df["rating"]
print(x)

# for index, row in df.iterrows():
#     x = x_backup
#     x = x.drop([index])
#     print(x)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, random_state=20, test_size=0.25, shuffle=True
)

# print(x_train.take([0, -1], axis=0))

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
df_player_rating_predictions["Test points"] = y
# Create a MinMaxScaler object
scaler = MinMaxScaler(feature_range=(0, 10))

# Scale the column
df["rating_mls_formula"] = scaler.fit_transform(
    df["rating_mls_formula"].values.reshape(-1, 1)
)

df_player_rating_predictions["Rating MLS Formula"] = df["rating_mls_formula"]


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

my_logger.print_logs_in_file("R2 on train")
my_logger.print_logs_in_file(str(DT_regressor.score(x_train, y_train)))

plot_prediction_vs_true_values(y_train, y_pred_dt, "train Decision Tree regressor")


# On test
y_pred_test = DT_regressor.predict(x_test)  # Predictions on Testing data

mean_squared_error(y_test, y_pred_test, squared=False)
MSE = np.square(np.subtract(y_test, y_pred_test)).mean()

RMSE = math.sqrt(MSE)
my_logger.print_logs_in_file(f"RMSE for Decision Tree Regresor on Test: {RMSE}")

my_logger.print_logs_in_file("R2 on test")
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


my_logger.print_logs_in_file("R2 on train")
my_logger.print_logs_in_file(str(RF_regressor.score(x_train, y_train)))

plot_prediction_vs_true_values(y_train, y_pred_dt, "train Random Forest regressor")

# On test
y_pred_test = RF_regressor.predict(x_test)  # Predictions on Testing data

mean_squared_error(y_test, y_pred_test, squared=False)
MSE = np.square(np.subtract(y_test, y_pred_test)).mean()

RMSE = math.sqrt(MSE)
my_logger.print_logs_in_file(f"RMSE for Random Forest on Test: {RMSE}")

my_logger.print_logs_in_file("R2 on test")
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

my_logger.print_logs_in_file("R2 on train")
my_logger.print_logs_in_file(str(XGB_Regressor.score(x_train, y_train)))

plot_prediction_vs_true_values(y_train, y_pred_xgb, "train XGBoost regressor")


# On test
y_pred_test = XGB_Regressor.predict(x_test)  # Predictions on Testing data

mean_squared_error(y_test, y_pred_test, squared=False)
MSE = np.square(np.subtract(y_test, y_pred_test)).mean()

RMSE = math.sqrt(MSE)
my_logger.print_logs_in_file(f"RMSE for XGBoost Regresor on Test: {RMSE}")

my_logger.print_logs_in_file("R2 on test")
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


my_logger.print_logs_in_file("R2 on train")
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

my_logger.print_logs_in_file("R2 on test")
my_logger.print_logs_in_file(str(P_Regressor.score(X_poly_test, y_test)))

my_logger.print_logs_in_file("")

plot_prediction_vs_true_values(y_test, y_pred_test, "test polynomial regressor")

df_player_rating_predictions["Polynomial points"] = y_pred_test


############################################################################################################
# SVR Regressor

# On train


svr = SVR(kernel="rbf", C=1.0, epsilon=0.1)
svr.fit(x_train, y_train)

svr.fit(x_train, y_train)

y_pred_pr = svr.predict(x_train)

mean_squared_error(y_train, y_pred_pr, squared=False)
MSE = np.square(np.subtract(y_train, y_pred_pr)).mean()

RMSE = math.sqrt(MSE)
my_logger.print_logs_in_file(f"RMSE for SVR regressor on Train: {RMSE}")


my_logger.print_logs_in_file("R2 on train")
my_logger.print_logs_in_file(str(svr.score(x_train, y_train)))

plot_prediction_vs_true_values(y_train, y_pred_pr, "train svr regressor")

# On test

svr.fit(x_test, y_test)

y_pred_test = svr.predict(x_test)  # Predictions on Testing data

mean_squared_error(y_test, y_pred_test, squared=False)
MSE = np.square(np.subtract(y_test, y_pred_test)).mean()

RMSE = math.sqrt(MSE)
my_logger.print_logs_in_file(f"RMSE for SVR Regresor on Test: {RMSE}")

my_logger.print_logs_in_file("R2 on test")
my_logger.print_logs_in_file(str(svr.score(x_test, y_test)))

my_logger.print_logs_in_file("")

plot_prediction_vs_true_values(y_test, y_pred_test, "test SVR regressor")

df_player_rating_predictions["SVR points"] = y_pred_test


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
score_svr = cross_val_score(
    svr, x, y, scoring="neg_mean_squared_error", cv=crossValidation, n_jobs=-1
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

RMSE = sqrt(mean(absolute(score_svr)))
my_logger.print_logs_in_file(f"RMSE for K-fold validation with SVR model: {RMSE}")
my_logger.print_logs_in_file("")


# view R2
# Define cross-validation method to use
# Use k-fold CV to evaluate model

score_dt = cross_val_score(
    DT_regressor, x, y, scoring="r2", cv=crossValidation, n_jobs=-1
)
score_rf = cross_val_score(
    RF_regressor, x, y, scoring="r2", cv=crossValidation, n_jobs=-1
)
score_xgb = cross_val_score(
    XGB_Regressor, x, y, scoring="r2", cv=crossValidation, n_jobs=-1
)
score_poly = cross_val_score(
    P_Regressor, x, y, scoring="r2", cv=crossValidation, n_jobs=-1
)
score_svr = cross_val_score(svr, x, y, scoring="r2", cv=crossValidation, n_jobs=-1)

# View R2 scores

R2 = mean(score_dt)
my_logger.print_logs_in_file(
    f"R2 scores for K-fold validation with Decision Tree model: {R2}"
)

R2 = mean(score_rf)
my_logger.print_logs_in_file(
    f"R2 scores for K-fold validation with Random Forest model: {R2}"
)

R2 = mean(score_xgb)
my_logger.print_logs_in_file(
    f"R2 scores for K-fold validation with XGBoost model: {R2}"
)

R2 = mean(score_poly)
my_logger.print_logs_in_file(
    f"R2 scores for K-fold validation with Polynomial model: {R2}"
)

R2 = mean(score_svr)
my_logger.print_logs_in_file(
    f"R2 scores for K-fold validation with Support Vector Regression model: {R2}"
)
my_logger.print_logs_in_file("")

my_logger.print_logs_in_file("end")

df_player_rating_predictions.to_csv("./converted_files/player_rating_predictors.csv")

from sklearn.feature_selection import RFE

# RECURSIVE FEATURE ELIMINATION FOR DECISION TREE
###########################################
# Initialize the RFE object with the regression model and the desired number of features to select
rfe_dt = RFE(
    estimator=DT_regressor, n_features_to_select=5
)  # Change the value of n_features_to_select as per your requirement

# Fit the RFE object to the data
rfe_dt.fit(x, y)

# Get the selected feature indices and column names
selected_feature_indices = rfe_dt.support_
selected_feature_names = x.columns[selected_feature_indices]
# selected_feature_names = [x[idx] for idx in selected_feature_indices]


# Print the selected features
print("Selected Features of decision tree regressor are:")
for feature in selected_feature_names:
    print(feature)
print()
print()


# RECURSIVE FEATURE ELIMINATION FOR RANDOM FOREST
###########################################
# Initialize the RFE object with the regression model and the desired number of features to select
rfe_rf = RFE(
    estimator=RF_regressor, n_features_to_select=5, importance_getter="auto"
)  # Change the value of n_features_to_select as per your requirement

# Fit the RFE object to the data
rfe_rf.fit(x, y)

# Get the selected feature indices and column names
selected_feature_indices = rfe_rf.support_
selected_feature_names = x.columns[selected_feature_indices]
# selected_feature_names = [x[idx] for idx in selected_feature_indices]


# Print the selected features
print("Selected Features of random forest regressor are:")
for feature in selected_feature_names:
    print(feature)
print()
print()

# RECURSIVE FEATURE ELIMINATION FOR XGBOOST
###########################################
# Initialize the RFE object with the regression model and the desired number of features to select
rfe_xgb = RFE(
    estimator=XGB_Regressor, n_features_to_select=5
)  # Change the value of n_features_to_select as per your requirement

# Fit the RFE object to the data
rfe_xgb.fit(x, y)

# Get the selected feature indices and column names
selected_feature_indices = rfe_xgb.support_
selected_feature_names = x.columns[selected_feature_indices]
# selected_feature_names = [x[idx] for idx in selected_feature_indices]


# Print the selected features
print("Selected Features of XGBoost regressor are:")
for feature in selected_feature_names:
    print(feature)
print()
print()


# # Fit the RFE object to the data
# rfe_xgb.fit(x, y)

# # Get the selected feature indices
# selected_feature_indices = rfe_xgb.support_

# # Get the feature importances from the XGBoost regressor
# feature_importances = rfe_xgb.estimator_.feature_importances_

# # Sort the selected features based on their importance scores
# selected_feature_names = x.columns[selected_feature_indices]
# selected_feature_names = selected_feature_names[np.argsort(feature_importances)][::-1]

# # Print the selected features in order of importance
# print("Selected Features of XGBoost regressor in order of importance:")
# for feature in selected_feature_names:
#     print(feature)
# print()
# print()

# RECURSIVE FEATURE ELIMINATION FOR POLYNOMIAL
###########################################
# Initialize the RFE object with the regression model and the desired number of features to select
rfe_polynomial = RFE(
    estimator=P_Regressor, n_features_to_select=5
)  # Change the value of n_features_to_select as per your requirement

# Fit the RFE object to the data
rfe_polynomial.fit(x, y)

# Get the selected feature indices and column names
selected_feature_indices = rfe_polynomial.support_
selected_feature_names = x.columns[selected_feature_indices]
# selected_feature_names = [x[idx] for idx in selected_feature_indices]


# Print the selected features
print("Selected Features of plynomial regressor are:")
for feature in selected_feature_names:
    print(feature)
print()
print()

# Lazy predictor
# clf = LazyRegressor(verbose=0, ignore_warnings=True, custom_metric=None)
# models, predictions = clf.fit(x_train, x_test, y_train, y_test)
# print(models)

# dump(XGB_Regressor, "XGBoostRegressor.joblib")
XGB_Regressor.save_model("xgboost_model_old_version.XGBoostRegressor")

# XGB_Regressor.save_model('XGBoostRegressor.json')
