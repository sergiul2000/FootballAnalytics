import pandas as pd

df = pd.read_csv("./converted_files/player_rating_predictors.csv")

dt_avg_delta_points = 0
rf_avg_delta_points = 0
xgb_avg_delta_points = 0
pl_avg_delta_points = 0
mls_avg_delta_points = 0
nr_of_rows = 0

hit_rate_dt = 0
hit_rate_rf = 0
hit_rate_xgb = 0
hit_rate_pol = 0
hit_rate_mls = 0


def caulculate_delta_points(real_points, predict, column_name):
    delta_points = abs(real_points - predict)
    df.at[index, column_name] = delta_points
    return delta_points


def caulculate_hits(real_points, predict):
    if real_points == predict:
        return 1
    return 0


def calculate_hit_procentage(part, whole):
    return 100 * float(part) / float(whole)


for index, row in df.iterrows():
    nr_of_rows += 1
    real_points = row["Test points"]
    dt_points = row["Decision tree points"]
    rf_points = row["Random forest points"]
    xgb_points = row["XGBoost points"]
    pl_points = row["Polynomial points"]
    mls_points = row["Rating MLS Formula"]

    dt_avg_delta_points += caulculate_delta_points(
        real_points, dt_points, "dt delta ponts"
    )

    rf_avg_delta_points += caulculate_delta_points(
        real_points, rf_points, "rf delta ponts"
    )

    xgb_avg_delta_points += caulculate_delta_points(
        real_points, xgb_points, "xgb delta ponts"
    )
    pl_avg_delta_points += caulculate_delta_points(
        real_points, pl_points, "pl delta ponts"
    )

    mls_avg_delta_points += caulculate_delta_points(
        real_points, mls_points, "mls delta ponts"
    )

    hit_rate_dt += caulculate_hits(real_points, dt_points)
    hit_rate_rf += caulculate_hits(real_points, rf_points)
    hit_rate_xgb += caulculate_hits(real_points, xgb_points)
    hit_rate_pol += caulculate_hits(real_points, pl_points)
    hit_rate_mls += caulculate_hits(real_points, mls_points)


dt_avg_delta_points /= nr_of_rows
rf_avg_delta_points /= nr_of_rows
xgb_avg_delta_points /= nr_of_rows
pl_avg_delta_points /= nr_of_rows
mls_avg_delta_points /= nr_of_rows
print("Avg delta points of Decision Tree is: " + str(dt_avg_delta_points))
print("Avg delta points of Random forest is: " + str(rf_avg_delta_points))
print("Avg delta points of XGBoost is: " + str(xgb_avg_delta_points))
print("Avg delta points of Polynomial is: " + str(pl_avg_delta_points))
print("Avg delta points of MLS Formula is: " + str(mls_avg_delta_points))

print("==============================================")
print()

print(
    "Nr. of exact predicts of Decision Tree is: "
    + str(caulculate_hits(hit_rate_dt, nr_of_rows))
)
print(
    "Nr. of exact predicts of Random Forest is: "
    + str(caulculate_hits(hit_rate_rf, nr_of_rows))
)
print(
    "Nr. of exact predicts of XGBoost is: "
    + str(caulculate_hits(hit_rate_xgb, nr_of_rows))
)
print(
    "Nr. of exact predicts of Polynomial is: "
    + str(caulculate_hits(hit_rate_pol, nr_of_rows))
)
print(
    "Nr. of exact predicts of MLS Formula is: "
    + str(caulculate_hits(hit_rate_mls, nr_of_rows))
)
# df.to_csv("./converted_files/models_analyzer_for_player_rating.csv")
