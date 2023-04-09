import pandas as pd

df = pd.read_csv("./converted_files/player_rating_predictors.csv")

dt_avg_delta_points = 0
rf_avg_delta_points = 0
xgb_avg_delta_points = 0
pl_avg_delta_points = 0
nr_of_rows = 0

for index, row in df.iterrows():
    nr_of_rows += 1
    real_points = row["Test points"]
    dt_points = row["Decision tree points"]
    rf_points = row["Random forest points"]
    xgb_points = row["XGBoost points"]
    pl_points = row["Polynomial points"]

    dt_delta_points = abs(real_points - dt_points)
    df.at[index, "dt delta ponts"] = dt_delta_points
    dt_avg_delta_points += dt_delta_points

    rf_delta_points = abs(real_points - rf_points)
    df.at[index, "rf delta ponts"] = rf_delta_points
    rf_avg_delta_points += rf_delta_points

    xgb_delta_points = abs(real_points - xgb_points)
    df.at[index, "xgb delta ponts"] = xgb_delta_points
    xgb_avg_delta_points += xgb_delta_points

    pl_delta_points = abs(real_points - pl_points)
    df.at[index, "pl delta ponts"] = pl_delta_points
    pl_avg_delta_points += pl_delta_points

dt_avg_delta_points /= nr_of_rows
rf_avg_delta_points /= nr_of_rows
xgb_avg_delta_points /= nr_of_rows
pl_avg_delta_points /= nr_of_rows
print("Avg delta points of Decision Tree is: " + str(dt_avg_delta_points))
print("Avg delta points of Random forest is: " + str(rf_avg_delta_points))
print("Avg delta points of XGBoost is: " + str(xgb_avg_delta_points))
print("Avg delta points of Polynomial is: " + str(pl_avg_delta_points))
# df.to_csv("./converted_files/models_analyzer_for_player_rating.csv")
